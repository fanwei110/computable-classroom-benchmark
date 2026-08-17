"""Analyze the Phase-C robustness experiments (runs/exp_results.csv):
  [A] template ablation — per-variant strict correctness + component
      contributions (unbundles the C4 "structure" factor);
  [B] temperature sensitivity — C1 vs C4 correctness across T in {0,0.5,1.0}.
Writes runs/exp_stats.txt. All on DeepSeek (deepseek-chat), 6 representative
tasks (one per KP), 5 reps. Correctness defined exactly as aggregate_formal.py.
"""
import io, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
out = []
def p(s=""): out.append(str(s)); print(s)

df = pd.read_csv(ROOT / "runs" / "exp_results.csv")
p("================================================================")
p("PHASE-C EXPERIMENTS  (DeepSeek deepseek-chat; 6 tasks x 5 reps)")
p(f"total rows = {len(df)}")
p("================================================================")

# ---------- [A] ablation ----------
abl = df[df.experiment == "ablation"]
order = ["C1", "contract_only", "minus_scaffold", "minus_convention", "C4_full"]
desc = {"C1": "raw improvised phrasing + contract",
        "contract_only": "structured task + contract (no framing/scaffold/conv)",
        "minus_scaffold": "full C4 minus step-scaffold",
        "minus_convention": "full C4 minus convention (~structure-only)",
        "C4_full": "full CKU template"}
p("\n[A] Template ablation — strict correctness by variant")
m = {}
for v in order:
    s = abl[abl.variant == v]
    if len(s):
        m[v] = 100 * s.correct.mean()
        p(f"  {v:18s} {m[v]:5.1f}%  (exec {100*s.exec_ok.mean():.0f}%, n={len(s)})  — {desc[v]}")
if set(order) <= set(m):
    p("\n  Component contributions (pp):")
    p(f"    raw -> structured task     (contract_only - C1) = {m['contract_only']-m['C1']:+.1f}")
    p(f"    add scaffold               (C4_full - minus_scaffold) = {m['C4_full']-m['minus_scaffold']:+.1f}")
    p(f"    add convention             (C4_full - minus_convention) = {m['C4_full']-m['minus_convention']:+.1f}")
    p(f"    structured -> full C4      (C4_full - contract_only) = {m['C4_full']-m['contract_only']:+.1f}")
    p(f"    total raw -> full C4       (C4_full - C1) = {m['C4_full']-m['C1']:+.1f}")

# ---------- [B] temperature ----------
tmp = df[df.experiment == "temperature"]
p("\n[B] Temperature sensitivity — strict correctness (%)")
p(f"  {'cond':10s}" + "".join(f"  T={t}" for t in sorted(tmp.temperature.dropna().unique())))
for cond in ["C1", "C4_full"]:
    s = tmp[tmp.variant == cond]
    cells = []
    for t in sorted(tmp.temperature.dropna().unique()):
        st = s[s.temperature == t]
        cells.append(f"{100*st.correct.mean():5.1f}" if len(st) else "   NA")
    p(f"  {cond:10s}" + "".join(f"  {c}" for c in cells))
p("\n  Read: if C4_full >> C1 at every temperature, the structure effect is not"
  "\n  a lucky-default artifact.")

(ROOT / "runs" / "exp_stats.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
p("\nwrote runs/exp_stats.txt")
