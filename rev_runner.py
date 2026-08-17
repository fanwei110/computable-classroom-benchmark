"""Revision-1 crossing experiment (reviewer R1.2): complete the wording x
scaffold factorial in the -convention row by adding the two missing cells.

    (improvised, no scaffold)  = C1    (existing formal data)
    (regularized, no scaffold) = Creg  (NEW: task statement + lib + contract)
    (improvised, scaffold)     = C1wS  (NEW: C2 scaffold, task block replaced
                                        by the VERBATIM frozen C1 phrasing)
    (regularized, scaffold)    = C2    (existing formal data)

Design notes (mirrors the frozen material exactly):
- Creg reuses the exp_runner "contract_only" composition (task + lib +
  contract) so it is consistent with the Section V.E ablation, but built from
  C2_zh (identical task/lib/contract blocks; verified in --dry).
- C1wS keeps the C1 phrasing verbatim (its own contract paragraph stripped,
  since the scaffold supplies the identical contract block) and swaps it in
  for the regularized task block of the C2_zh scaffold. Persona variants A/B
  alternate across replay repetitions. This preserves the same two frozen
  variants and five uses of each, although the original formal runs were
  submitted as two five-repetition blocks rather than in alternating order.
- Generation + judging + logging reuse runner.run_one unchanged (frozen
  judge, frozen decoding policy, full JSONL with usage).
- Post-hoc, disclosed experiment (deviation log #11); changes nothing in the
  preregistered pipeline. Resume-safe: existing run_ids are skipped.

Usage:
  python rev_runner.py --dry                       # build prompts only
  python rev_runner.py --key-file <path> --reps 5  # pilot (6 tasks)
  python rev_runner.py --key-file <path> --reps 10 --tasks all --tag rev_full
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from runner import run_one  # noqa: E402  (frozen judge + OpenRouter machinery)

# same representative subset as exp_runner.py (one per knowledge point)
PILOT_TASKS = ["KP1_T1", "KP2_T3", "KP3_T1", "KP4_T1", "KP5_T3", "KP6_T1"]
CONDITIONS = ["Creg", "C1wS"]
# 对两个预注册单元做短窗口复跑（reviewer B01 fix）。新单元在8月4—5日采集，
# C1/C2复跑在8月6日采集；该设计缩短但不消除日期与路由差异。复跑提示与冻结
# 正式材料逐字节一致，变化的是采集时点及可能的服务商路由。
BATCH_CONDITIONS = ["C1rep", "C2rep"]


def blocks_of(text):
    """Label the blank-line-separated blocks of a frozen C2_zh prompt."""
    out = {}
    for para in [p.strip() for p in text.split("\n\n") if p.strip()]:
        if para.startswith("你是"):
            out["role"] = para
        elif para.startswith("概念"):
            out["concept"] = para
        elif para.startswith("假设处理"):
            out["assume"] = para
        elif para.startswith("任务"):
            out["task"] = para
        elif para.startswith("请按以下步骤"):
            out["scaffold"] = para
        elif para.startswith("写一"):
            out["lib"] = para
        elif para.startswith("输出契约"):
            out["contract"] = para
        else:
            out.setdefault("other", []).append(para)
    return out


def c1_phrase(task_id, variant_letter):
    """Verbatim frozen improvised phrasing, its contract paragraph stripped."""
    text = (ROOT / "prompts" / "C1_final" / f"{task_id}_{variant_letter}.md"
            ).read_text(encoding="utf-8")
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    kept = [p for p in paras if not p.startswith("输出契约")]
    return "\n\n".join(kept)


def build_prompt(condition, task_id, variant_letter="A"):
    # C1rep / C2rep: byte-identical replays of the frozen formal prompts,
    # collected in the adjacent replay window after Creg/C1wS (no reconstruction).
    if condition == "C1rep":
        return (ROOT / "prompts" / "C1_final" / f"{task_id}_{variant_letter}.md"
                ).read_text(encoding="utf-8")
    if condition == "C2rep":
        return (ROOT / "prompts" / "C2_zh" / f"{task_id}.md"
                ).read_text(encoding="utf-8")
    b = blocks_of((ROOT / "prompts" / "C2_zh" / f"{task_id}.md"
                   ).read_text(encoding="utf-8"))
    if condition == "Creg":      # regularized statement, no scaffold
        parts = [b["task"], b["lib"], b["contract"]]
    elif condition == "C1wS":    # verbatim improvised phrasing inside scaffold
        parts = [b["role"], b["concept"], b["assume"],
                 c1_phrase(task_id, variant_letter),
                 b["scaffold"], b["lib"], b["contract"]]
    else:
        raise ValueError(condition)
    return "\n\n".join(parts) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="rev_pilot")
    ap.add_argument("--models", default="M1,M2,M3")
    ap.add_argument("--tasks", default="pilot", help="'pilot' (6), 'all' (18), or list")
    ap.add_argument("--reps", type=int, default=5)
    ap.add_argument("--conditions", default="new",
                    help="'new' (Creg,C1wS) | 'batch' (C1rep,C2rep) | comma list")
    ap.add_argument("--key-file")
    ap.add_argument("--dry", action="store_true",
                    help="build + save all prompts, call no API")
    args = ap.parse_args()

    if args.tasks == "pilot":
        task_ids = PILOT_TASKS
    elif args.tasks == "all":
        task_ids = sorted(p.stem for p in (ROOT / "tasks").glob("KP*_T*.yaml"))
    else:
        task_ids = args.tasks.split(",")
    models = args.models.split(",")

    outdir = ROOT / "runs" / "raw" / args.tag
    outdir.mkdir(parents=True, exist_ok=True)
    log_path = outdir / f"{args.tag}.jsonl"

    if args.dry:
        pv = outdir / "prompt_preview"
        pv.mkdir(exist_ok=True)
        n = 0
        for t in task_ids:
            (pv / f"{t}_Creg.md").write_text(build_prompt("Creg", t),
                                             encoding="utf-8")
            for v in ("A", "B"):
                (pv / f"{t}_C1wS_{v}.md").write_text(
                    build_prompt("C1wS", t, v), encoding="utf-8")
            n += 3
        # consistency check: C2_zh vs C4_zh task/lib/contract blocks identical
        import difflib  # noqa: F401
        mism = []
        for t in task_ids:
            b2 = blocks_of((ROOT / "prompts" / "C2_zh" / f"{t}.md").read_text(encoding="utf-8"))
            b4 = blocks_of((ROOT / "prompts" / "C4_zh" / f"{t}.md").read_text(encoding="utf-8"))
            for k in ("task", "lib", "contract"):
                if b2.get(k) != b4.get(k):
                    mism.append(f"{t}:{k}")
        print(f"dry run: wrote {n} prompt previews -> {pv}")
        print("C2_zh/C4_zh task-lib-contract identical: "
              + ("YES" if not mism else f"MISMATCH {mism}"))
        return

    key_text = Path(args.key_file).read_text(encoding="utf-8")
    api_key = re.search(r"sk-or-[\w-]+", key_text).group(0)

    done = set()
    if log_path.exists():
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                try:
                    done.add(json.loads(line)["run_id"])
                except Exception:  # noqa: BLE001
                    pass

    if args.conditions == "new":
        conds = CONDITIONS
    elif args.conditions == "batch":
        conds = BATCH_CONDITIONS
    else:
        conds = args.conditions.split(",")

    jobs = []
    for t in task_ids:
        for cond in conds:
            for m in models:
                for rep in range(1, args.reps + 1):
                    # 含即兴措辞的单元在复跑中交替使用 A/B，各5次；正式实验则
                    # 分两个5次重复块提交。两者提示多重集相同，调用顺序不同。
                    # 只有单一规范提示的 Creg/C2rep 始终记作 A。
                    v = ("A" if (cond in ("Creg", "C2rep") or rep % 2 == 1)
                         else "B")
                    run_id = f"{m}_{cond}_{t}_v{v}_r{rep:02d}"
                    if run_id not in done:
                        jobs.append((run_id, m, cond, t, v))
    print(f"to run: {len(jobs)} (skipping {len(done)} already done)")

    n_ok = n_fail = 0
    with open(log_path, "a", encoding="utf-8") as log:
        for i, (run_id, m, cond, t, v) in enumerate(jobs, 1):
            prompt = build_prompt(cond, t, v)
            try:
                rec = run_one(run_id, m, cond, t, prompt, api_key, outdir)
                log.write(json.dumps(rec, ensure_ascii=False) + "\n")
                log.flush()
                n_ok += 1
                j = rec["judge"]
                print(f"[{i}/{len(jobs)}] {run_id}: bucket={j['bucket']} "
                      f"api={rec['latency_s']['api']}s")
            except Exception as e:  # noqa: BLE001
                n_fail += 1
                print(f"[FAIL] {run_id}: {e}")
    print(f"\ndone: {n_ok} ok, {n_fail} failed -> {log_path}")


if __name__ == "__main__":
    main()
