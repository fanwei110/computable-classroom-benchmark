"""Stage-2 generation runner.

Calls the configured models via OpenRouter, executes and judges each
generation with the frozen harness, and archives everything per
runs/schema.md (JSONL + per-run code files under runs/raw/<tag>/).

Safety rails:
- refuses to run unless config/models.yaml has locked: true;
- refuses to run C1/C3 in formal mode unless prompts/C1_final exists
  (i.e., the external phrasings have been collected and frozen); pilot
  runs must pass an explicit --phrasings file and a --tag other than
  'formal';
- the API key is read from --key-file or the OPENROUTER_API_KEY env var
  and is never written to any log or output;
- transport errors are retried per config; model-content failures never.

Usage examples:
  python runner.py --tag pilot --models M1,M2,M3 --conditions C4 \
      --tasks KP1_T1 --reps 1
  python runner.py --tag pilot --models M1 --conditions C1,C3 \
      --tasks KP5_T3 --reps 1 \
      --phrasings prompts/pilot_simulated/teacher_A_simulated.md --variant 1
"""

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "harness"))
from judge import judge  # noqa: E402

CONFIG = yaml.safe_load((ROOT / "config" / "models.yaml").read_text(encoding="utf-8"))
HEADER_ZH = (ROOT / "prompts" / "convention_header_zh.txt").read_text(encoding="utf-8").strip()


def output_contract_zh(spec):
    keys = ", ".join(f"'{k}'" for k in spec["required_keys"])
    line = f"输出契约：把所有要求的输出存入名为 `result` 的字典，键名严格为：{keys}。"
    if spec["figure_required"]:
        line += " 将图保存为文件，并把文件路径存入 result['figure_path']。"
    return line


def load_task(task_id):
    return yaml.safe_load((ROOT / "tasks" / f"{task_id}.yaml").read_text(encoding="utf-8"))


def parse_phrasings(path):
    """{task_id: [v1, v2]} from a (real or simulated) collection file."""
    text = Path(path).read_text(encoding="utf-8")
    out = {}
    blocks = re.split(r"^### (KP\d_T\d)", text, flags=re.M)[1:]
    for task_id, body in zip(blocks[0::2], blocks[1::2]):
        v1 = re.search(r"^V1:\s*(.+?)(?=^V2:)", body, re.M | re.S)
        v2 = re.search(r"^V2:\s*(.+?)(?=^###|\Z)", body, re.M | re.S)
        out[task_id] = [m.group(1).strip() for m in (v1, v2) if m]
    return out


def build_prompt(condition, task_id, phrasings=None, variant=1):
    spec = load_task(task_id)
    if condition in ("C2", "C4"):
        folder = "C2_zh" if condition == "C2" else "C4_zh"
        return (ROOT / "prompts" / folder / f"{task_id}.md").read_text(encoding="utf-8")
    phrase = phrasings[task_id][variant - 1]
    if condition == "C1":
        return f"{phrase}\n\n{output_contract_zh(spec)}\n"
    if condition == "C3":
        return f"{phrase}\n\n{HEADER_ZH}\n\n{output_contract_zh(spec)}\n"
    raise ValueError(condition)


def call_openrouter(model_slug, prompt, api_key):
    """One chat completion; returns (text, meta, api_latency_s). Retries
    transport-level failures per config; never retries model content."""
    url = CONFIG["api"]["base_url"].rstrip("/") + "/chat/completions"
    body = {
        "model": model_slug,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": CONFIG["decoding"]["max_tokens"],
    }
    headers = {"Authorization": f"Bearer {api_key}",
               "Content-Type": "application/json"}
    backoffs = CONFIG["api"]["retry_backoff_seconds"]
    last_err = None
    for attempt in range(CONFIG["api"]["max_retries"] + 1):
        try:
            t0 = time.perf_counter()
            resp = requests.post(url, json=body, headers=headers,
                                 timeout=CONFIG["api"]["timeout_seconds"])
            latency = time.perf_counter() - t0
            if resp.status_code in (429, 500, 502, 503, 504):
                last_err = f"HTTP {resp.status_code}: {resp.text[:200]}"
            else:
                resp.raise_for_status()
                data = resp.json()
                if "choices" not in data or not data["choices"]:
                    raise RuntimeError(f"no choices in response: {str(data)[:300]}")
                text = data["choices"][0]["message"]["content"] or ""
                meta = {"provider": data.get("provider"),
                        "model_id": data.get("model"),
                        "usage": data.get("usage"),
                        "finish_reason": data["choices"][0].get("finish_reason")}
                return text, meta, latency
        except (requests.RequestException, ValueError) as e:
            last_err = repr(e)
        if attempt < CONFIG["api"]["max_retries"]:
            time.sleep(backoffs[min(attempt, len(backoffs) - 1)])
    raise RuntimeError(f"API failed after retries: {last_err}")


CODE_FENCE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.S)


def extract_code(completion):
    """Frozen extraction rule: first fenced python block; else, if the text
    looks like bare code, the whole completion; else empty."""
    m = CODE_FENCE.search(completion)
    if m:
        return m.group(1)
    if re.search(r"^\s*(import|from)\s+\w+", completion, re.M) and \
            "result" in completion:
        return completion
    return ""


def run_one(run_id, model_key, condition, task_id, prompt, api_key, outdir):
    slug = CONFIG["models"][model_key]["openrouter_slug"]
    completion, meta, api_s = call_openrouter(slug, prompt, api_key)

    code = extract_code(completion)
    code_path = outdir / "code" / f"{run_id}.py"
    comp_path = outdir / "completions" / f"{run_id}.txt"
    code_path.parent.mkdir(parents=True, exist_ok=True)
    comp_path.parent.mkdir(parents=True, exist_ok=True)
    comp_path.write_text(completion, encoding="utf-8")

    t0 = time.perf_counter()
    if code.strip():
        code_path.write_text(code, encoding="utf-8")
        verdict = judge(task_id, code_path=code_path, completion_path=comp_path)
    else:
        verdict = judge(task_id, code_path=None, completion_path=comp_path)
    exec_s = time.perf_counter() - t0

    return {
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model": model_key,
        "model_label": CONFIG["models"][model_key]["label"],
        "model_slug": slug,
        "api_response_meta": meta,
        "condition": condition,
        "task_id": task_id,
        "prompt": prompt,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "decoding_policy": CONFIG["decoding"]["policy"],
        "completion": completion,
        "code_extracted": bool(code.strip()),
        "judge": verdict,
        "latency_s": {"api": round(api_s, 2), "exec_judge": round(exec_s, 2),
                      "total": round(api_s + exec_s, 2)},
        "manual_review": None, "error_class": None, "declared": None,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True, help="run tag; 'formal' is guarded")
    ap.add_argument("--models", default="M1,M2,M3")
    ap.add_argument("--conditions", required=True)
    ap.add_argument("--tasks", required=True, help="comma list or 'all'")
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--phrasings", help="phrasing file for C1/C3 (pilot) or "
                                        "omit in formal mode (uses C1_final)")
    ap.add_argument("--variant", type=int, default=1, choices=[1, 2])
    ap.add_argument("--key-file", help="file containing the API key "
                                       "(never logged); else env OPENROUTER_API_KEY")
    args = ap.parse_args()

    if not CONFIG.get("locked"):
        sys.exit("config/models.yaml is not locked; refusing to run (prereg rule)")

    conditions = args.conditions.split(",")
    if args.tag == "formal" and any(c in ("C1", "C3") for c in conditions):
        if not (ROOT / "prompts" / "C1_final").exists():
            sys.exit("formal C1/C3 requires frozen external phrasings in "
                     "prompts/C1_final (scenario-4 rule); not found")
    phrasings = parse_phrasings(args.phrasings) if args.phrasings else None
    if any(c in ("C1", "C3") for c in conditions) and phrasings is None \
            and args.tag != "formal":
        sys.exit("pilot C1/C3 needs --phrasings <file>")

    if args.key_file:
        api_key = Path(args.key_file).read_text(encoding="utf-8")
        api_key = re.search(r"sk-or-[\w-]+", api_key).group(0)
    else:
        import os
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        sys.exit("no API key (use --key-file or OPENROUTER_API_KEY)")

    task_ids = (sorted(p.stem for p in (ROOT / "tasks").glob("KP*_T*.yaml"))
                if args.tasks == "all" else args.tasks.split(","))
    models = args.models.split(",")

    outdir = ROOT / "runs" / "raw" / args.tag
    outdir.mkdir(parents=True, exist_ok=True)
    log_path = outdir / f"{args.tag}.jsonl"

    n_done, n_fail = 0, 0
    with open(log_path, "a", encoding="utf-8") as log:
        for task_id in task_ids:
            for cond in conditions:
                prompt = build_prompt(cond, task_id, phrasings, args.variant)
                for model_key in models:
                    for rep in range(1, args.reps + 1):
                        run_id = f"{model_key}_{cond}_{task_id}_v{args.variant}_r{rep:02d}"
                        try:
                            rec = run_one(run_id, model_key, cond, task_id,
                                          prompt, api_key, outdir)
                            log.write(json.dumps(rec, ensure_ascii=False) + "\n")
                            log.flush()
                            n_done += 1
                            j = rec["judge"]
                            print(f"[{n_done}] {run_id}: bucket={j['bucket']}"
                                  f"{' tier=' + j['tier'] if j['tier'] else ''} "
                                  f"api={rec['latency_s']['api']}s")
                        except Exception as e:  # noqa: BLE001
                            n_fail += 1
                            print(f"[FAIL] {run_id}: {e}")
    print(f"\ndone: {n_done} ok, {n_fail} failed -> {log_path}")


if __name__ == "__main__":
    main()
