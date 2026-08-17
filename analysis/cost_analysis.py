"""Deployment economics: tokens & latency PER CORRECT output, by condition.
Pricing-free (tokens, not $) and robust: structural prompting costs more tokens
per generation (longer template) but FEWER per CORRECT output, because far fewer
retries are needed. Reads runs/raw/formal/formal.jsonl (API usage) +
runs/results_formal.csv (latency). Writes runs/cost_stats.txt.
"""
import io, json, sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
out = []
def p(s=""): out.append(str(s)); print(s)

LOG = ROOT / "runs" / "raw" / "formal" / "formal.jsonl"
rows = []
for i, line in enumerate(LOG.read_text(encoding="utf-8").splitlines()):
    r = json.loads(line)
    meta = r.get("api_response_meta") or {}
    usage = meta.get("usage") or {}
    if i == 0:
        p(f"usage keys: {list(usage.keys())}")
    rows.append({"condition": r["condition"],
                 "correct": int(r["judge"]["bucket"] == "correct"),
                 "pt": usage.get("prompt_tokens"), "ct": usage.get("completion_tokens"),
                 "tt": usage.get("total_tokens"), "cost": usage.get("cost")})
df = pd.DataFrame(rows)
# fall back total = prompt+completion if total missing
df["tt"] = df["tt"].fillna(df["pt"].fillna(0) + df["ct"].fillna(0))
cov = df["tt"].gt(0).mean()
p(f"n={len(df)}  token-coverage={100*cov:.1f}%")

lat = pd.read_csv(ROOT / "runs" / "results_formal.csv")
p("\n=== Deployment economics by condition (tokens & latency per CORRECT output) ===")
p(f"{'cond':>4} {'acc%':>6} {'tok/gen':>8} {'in/out':>10} {'tok/correct':>12} {'gens/correct':>13} {'medLat':>7} {'~s/correct':>10}")
for cond in ("C1", "C2", "C3", "C4"):
    s = df[df.condition == cond]
    n, nc = len(s), int(s.correct.sum())
    tt, pt, ct = s.tt.sum(), s.pt.sum(), s.ct.sum()
    med = lat[lat.condition == cond].latency_total_s.median()
    acc = 100 * nc / n
    cost = s["cost"].fillna(0).sum()
    p(f"{cond:>4} {acc:6.1f} {tt/n:8.0f} {int(pt/n):>4}/{int(ct/n):<4} {tt/nc:12.0f} {n/nc:13.2f} {med:7.1f} {med*n/nc:10.0f}  ${cost:.3f}tot ${cost/nc:.4f}/correct")
p(f"\ntotal API cost of the 2,160-generation formal run: ${df['cost'].fillna(0).sum():.2f}")

p("\nRead: C4 uses more tokens PER GENERATION (longer template) but the improvised")
p("condition needs ~C1_gens/C4_gens as many attempts per correct output, so structure")
p("is cheaper PER CORRECT ANSWER on both tokens and wall-clock.")
(ROOT / "runs" / "cost_stats.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
p("\nwrote runs/cost_stats.txt")
