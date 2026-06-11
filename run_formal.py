"""Formal stage-2 run: 18 tasks x 4 conditions x 3 models x 10 reps = 2,160.

Repetition structure (per locked config):
  C1/C3: 2 frozen phrasing variants per task (persona A, persona B from
         prompts/C1_final, C3_final), 5 repetitions each.
  C2/C4: canonical zh prompt, 10 repetitions.

Engineering:
  - API calls run on a small thread pool (the slow part, ~10-45 s each);
  - code execution + judging run SEQUENTIALLY in the main thread, so
    concurrent generations can never race on figure files (the frozen
    harness executes with cwd = repo root);
  - resume-safe: run_ids already present in formal.jsonl are skipped, so
    the script can be re-launched after any interruption;
  - API-transport failures (after the config's retries) go to
    formal_failures.jsonl and are retried simply by re-running the script.

Usage:
  python run_formal.py --key-file <path> [--workers 6] [--max-jobs N]
"""

import argparse
import json
import queue
import re
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from runner import (CONFIG, build_prompt, call_openrouter, extract_code,  # noqa: E402
                    load_task)
sys.path.insert(0, str(ROOT / "harness"))
from judge import judge  # noqa: E402

import hashlib  # noqa: E402
from datetime import datetime, timezone  # noqa: E402

OUTDIR = ROOT / "runs" / "raw" / "formal"
LOG = OUTDIR / "formal.jsonl"
FAILLOG = OUTDIR / "formal_failures.jsonl"
STATUS = OUTDIR / "status.txt"


def formal_prompt(cond, task_id, variant):
    if cond in ("C2", "C4"):
        return build_prompt(cond, task_id)
    folder = "C1_final" if cond == "C1" else "C3_final"
    return (ROOT / "prompts" / folder / f"{task_id}_{variant}.md").read_text(
        encoding="utf-8")


def build_jobs():
    task_ids = sorted(p.stem for p in (ROOT / "tasks").glob("KP*_T*.yaml"))
    jobs = []
    for task_id in task_ids:
        for cond in ("C1", "C2", "C3", "C4"):
            if cond in ("C1", "C3"):
                slots = [("A", r) for r in range(1, 6)] + \
                        [("B", r) for r in range(6, 11)]
            else:
                slots = [("can", r) for r in range(1, 11)]
            for variant, rep in slots:
                for model in ("M1", "M2", "M3"):
                    run_id = f"{model}_{cond}_{task_id}_{variant}_r{rep:02d}"
                    jobs.append({"run_id": run_id, "model": model,
                                 "cond": cond, "task_id": task_id,
                                 "variant": variant, "rep": rep})
    # broad early coverage: first repetition of everything first
    jobs.sort(key=lambda j: (j["rep"], j["task_id"], j["cond"], j["model"]))
    return jobs


def done_ids():
    ids = set()
    if LOG.exists():
        for line in LOG.read_text(encoding="utf-8").splitlines():
            try:
                ids.add(json.loads(line)["run_id"])
            except (json.JSONDecodeError, KeyError):
                continue
    return ids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--key-file", required=True)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--max-jobs", type=int, default=0)
    args = ap.parse_args()

    if not CONFIG.get("locked"):
        sys.exit("config not locked; refusing to run")
    for need in ("C1_final", "C3_final", "C2_zh", "C4_zh"):
        if not (ROOT / "prompts" / need).exists():
            sys.exit(f"missing frozen prompt set prompts/{need}")

    api_key = re.search(r"sk-or-[\w-]+",
                        Path(args.key_file).read_text(encoding="utf-8")).group(0)

    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "code").mkdir(exist_ok=True)
    (OUTDIR / "completions").mkdir(exist_ok=True)

    done = done_ids()
    jobs = [j for j in build_jobs() if j["run_id"] not in done]
    if args.max_jobs:
        jobs = jobs[:args.max_jobs]
    total_grid = 2160
    print(f"grid={total_grid}, already done={len(done)}, to run now={len(jobs)}")
    if not jobs:
        print("nothing to do")
        return

    job_q = queue.Queue()
    for j in jobs:
        job_q.put(j)
    result_q = queue.Queue(maxsize=args.workers * 2)
    stop = threading.Event()

    def worker():
        while not stop.is_set():
            try:
                j = job_q.get_nowait()
            except queue.Empty:
                return
            prompt = formal_prompt(j["cond"], j["task_id"], j["variant"])
            try:
                completion, meta, api_s = call_openrouter(
                    CONFIG["models"][j["model"]]["openrouter_slug"], prompt, api_key)
                result_q.put(("ok", j, prompt, completion, meta, api_s))
            except Exception as e:  # noqa: BLE001
                result_q.put(("apifail", j, prompt, repr(e), None, None))

    threads = [threading.Thread(target=worker, daemon=True)
               for _ in range(args.workers)]
    for t in threads:
        t.start()

    n_total, n_fail, t_start = 0, 0, time.time()
    buckets = {}
    with open(LOG, "a", encoding="utf-8") as log, \
            open(FAILLOG, "a", encoding="utf-8") as faillog:
        expected = len(jobs)
        while n_total + n_fail < expected:
            kind, j, prompt, payload, meta, api_s = result_q.get()
            if kind == "apifail":
                n_fail += 1
                faillog.write(json.dumps(
                    {"run_id": j["run_id"], "error": payload,
                     "ts": datetime.now(timezone.utc).isoformat()},
                    ensure_ascii=False) + "\n")
                faillog.flush()
                print(f"[APIFAIL] {j['run_id']}: {payload[:120]}")
                continue
            completion = payload
            code = extract_code(completion)
            code_path = OUTDIR / "code" / f"{j['run_id']}.py"
            comp_path = OUTDIR / "completions" / f"{j['run_id']}.txt"
            comp_path.write_text(completion, encoding="utf-8")
            t0 = time.perf_counter()
            if code.strip():
                code_path.write_text(code, encoding="utf-8")
                verdict = judge(j["task_id"], code_path=code_path,
                                completion_path=comp_path)
            else:
                verdict = judge(j["task_id"], code_path=None,
                                completion_path=comp_path)
            exec_s = time.perf_counter() - t0
            rec = {
                "run_id": j["run_id"],
                "timestamp_utc": datetime.now(timezone.utc).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"),
                "model": j["model"],
                "model_label": CONFIG["models"][j["model"]]["label"],
                "model_slug": CONFIG["models"][j["model"]]["openrouter_slug"],
                "api_response_meta": meta,
                "condition": j["cond"], "task_id": j["task_id"],
                "variant": j["variant"], "repetition": j["rep"],
                "prompt": prompt,
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "decoding_policy": CONFIG["decoding"]["policy"],
                "completion": completion,
                "code_extracted": bool(code.strip()),
                "judge": verdict,
                "latency_s": {"api": round(api_s, 2),
                              "exec_judge": round(exec_s, 2),
                              "total": round(api_s + exec_s, 2)},
                "manual_review": None, "error_class": None, "declared": None,
            }
            log.write(json.dumps(rec, ensure_ascii=False) + "\n")
            log.flush()
            n_total += 1
            b = verdict["bucket"]
            buckets[b] = buckets.get(b, 0) + 1
            if n_total % 25 == 0 or n_total == expected:
                elapsed = time.time() - t_start
                rate = n_total / elapsed * 3600
                eta_h = (expected - n_total - n_fail) / max(rate, 1) if rate else 0
                line = (f"{n_total}/{expected} done ({n_fail} api-fail) "
                        f"| {rate:.0f}/h | eta {eta_h:.1f}h | {buckets}")
                print(line)
                STATUS.write_text(
                    f"{datetime.now().isoformat()}\n{line}\n", encoding="utf-8")

    stop.set()
    print(f"\nFINISHED: {n_total} logged, {n_fail} api-failures "
          f"(re-run to retry failures). buckets={buckets}")


if __name__ == "__main__":
    main()
