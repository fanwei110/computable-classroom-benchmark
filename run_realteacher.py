"""Real-teacher validation batch (paper §IV.C).

Assembles C1/C3 prompts from the two real-instructor phrasing files, screens
them for convention leaks (same word-level screen as the persona set), runs
10 tasks x {C1,C3} x 3 models x 5 reps = 300 generations through the frozen
harness, and archives to runs/raw/realteacher/realteacher.jsonl.

Variant mapping mirrors the persona design (2 phrasing variants x 5 reps per
task-condition): teacher A = variant "rtA", teacher B = variant "rtB".
Resume-safe. Usage: python run_realteacher.py --key-file <path> [--workers 6]
"""

import argparse
import hashlib
import json
import queue
import re
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from runner import CONFIG, call_openrouter, extract_code, output_contract_zh, load_task  # noqa: E402
sys.path.insert(0, str(ROOT / "harness"))
from judge import judge  # noqa: E402

PROMPTS = ROOT / "prompts" / "real_teacher"
HEADER_ZH = (ROOT / "prompts" / "convention_header_zh.txt").read_text(encoding="utf-8").strip()
OUTDIR = ROOT / "runs" / "raw" / "realteacher"
LOG = OUTDIR / "realteacher.jsonl"

# same word-level convention screen used on the persona phrasings
LEAK = [r"\b252\b", r"\b250\b", r"\b365\b", r"交易日", r"日历日", r"自然日",
        r"复利", r"ddof", r"样本标准差", r"总体标准差", r"单尾", r"双尾",
        r"线性插值", r"布林森", r"Brinson", r"几何平均折算", r"小数表示",
        r"百分比表示"]


def parse(path):
    text = Path(path).read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"^### (KP\d_T\d)\s*\nV1:\s*(.+)$", text, re.M):
        out[m.group(1)] = m.group(2).strip()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key-file", required=True)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    api_key = re.search(r"sk-or-[\w-]+",
                        Path(args.key_file).read_text(encoding="utf-8")).group(0)

    pA = parse(PROMPTS / "teacher_real_A.md")
    pB = parse(PROMPTS / "teacher_real_B.md")
    tasks = sorted(set(pA) & set(pB))
    assert len(tasks) == 10, f"expected 10 shared tasks, got {len(tasks)}"

    # leak screen
    leaks = []
    for who, d in (("A", pA), ("B", pB)):
        for t, ph in d.items():
            for pat in LEAK:
                if re.search(pat, ph, re.I):
                    leaks.append(f"{who}/{t}: '{pat}'")
    if leaks:
        print("CONVENTION LEAKS — fix before running:")
        for x in leaks:
            print("  " + x)
        sys.exit(1)
    print(f"leak screen clean; {len(tasks)} tasks x C1/C3 x 3 models x 5 reps = "
          f"{len(tasks)*2*3*5} generations")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "code").mkdir(exist_ok=True)
    (OUTDIR / "completions").mkdir(exist_ok=True)
    done = set()
    if LOG.exists():
        for line in LOG.read_text(encoding="utf-8").splitlines():
            try:
                done.add(json.loads(line)["run_id"])
            except Exception:  # noqa: BLE001
                pass

    def build(cond, task_id, variant):
        ph = (pA if variant == "rtA" else pB)[task_id]
        spec = load_task(task_id)
        contract = output_contract_zh(spec)
        if cond == "C1":
            return f"{ph}\n\n{contract}\n"
        return f"{ph}\n\n{HEADER_ZH}\n\n{contract}\n"

    jobs = []
    for task_id in tasks:
        for cond in ("C1", "C3"):
            for variant in ("rtA", "rtB"):
                for rep in range(1, 6):
                    rid = f"{{m}}_{cond}_{task_id}_{variant}_r{rep:02d}"
                    for model in ("M1", "M2", "M3"):
                        run_id = rid.format(m=model)
                        if run_id not in done:
                            jobs.append((run_id, model, cond, task_id, variant, rep))
    print(f"to run now: {len(jobs)}")

    q = queue.Queue()
    for j in jobs:
        q.put(j)
    lock = threading.Lock()
    cnt = {"n": 0, "fail": 0}

    def worker():
        while True:
            try:
                run_id, model, cond, task_id, variant, rep = q.get_nowait()
            except queue.Empty:
                return
            prompt = build(cond, task_id, variant)
            try:
                completion, meta, api_s = call_openrouter(
                    CONFIG["models"][model]["openrouter_slug"], prompt, api_key)
            except Exception as e:  # noqa: BLE001
                with lock:
                    cnt["fail"] += 1
                    print(f"[APIFAIL] {run_id}: {repr(e)[:80]}")
                continue
            code = extract_code(completion)
            cp = OUTDIR / "completions" / f"{run_id}.txt"
            cp.write_text(completion, encoding="utf-8")
            if code.strip():
                kp = OUTDIR / "code" / f"{run_id}.py"
                kp.write_text(code, encoding="utf-8")
                verdict = judge(task_id, code_path=kp, completion_path=cp)
            else:
                verdict = judge(task_id, code_path=None, completion_path=cp)
            rec = {"run_id": run_id, "timestamp_utc": datetime.now(timezone.utc)
                   .strftime("%Y-%m-%dT%H:%M:%SZ"), "model": model,
                   "condition": cond, "task_id": task_id, "variant": variant,
                   "repetition": rep, "source": "real_teacher",
                   "prompt": prompt,
                   "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                   "completion": completion, "code_extracted": bool(code.strip()),
                   "judge": verdict, "latency_s": {"api": round(api_s, 2)}}
            with lock:
                with open(LOG, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                cnt["n"] += 1
                if cnt["n"] % 25 == 0:
                    print(f"{cnt['n']}/{len(jobs)} ({cnt['fail']} apifail)", flush=True)

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(args.workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"FINISHED: {cnt['n']} logged, {cnt['fail']} api failures")


if __name__ == "__main__":
    main()
