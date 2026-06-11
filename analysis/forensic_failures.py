"""Forensic pass over numeric_wrong generations: mechanically probe which
known convention swap (if any) explains each failed key, using the
value/reference ratios stored in the judge details.

Probes (ratio = submitted / reference, on the first failed numeric key):
  x100 / /100      percent-vs-decimal units
  -1               sign convention
  ~0.8309 / ~1.2035  365-day de-annualization (sqrt(252/365) and inverse)
  ~1.0040 / ~0.9960  250-day annualization
  ~1.1915           z=1.96 instead of 1.645 (one-day VaR)
  close (<2e-3)     near-miss: intermediate rounding / hand arithmetic
  other             everything else (candidate conceptual/code issues)

This is exploratory tooling for the error-coding stage - NOT a judging
change. Output: counts by condition and by model, plus per-pattern examples.
"""

import io
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "runs" / "raw" / "formal" / "formal.jsonl"

PATTERNS = [
    ("x100", lambda q: abs(q - 100) < 0.5),
    ("/100", lambda q: abs(q - 0.01) < 5e-5),
    ("sign", lambda q: abs(q + 1) < 1e-3),
    ("365d", lambda q: abs(q - 0.83088) < 2e-3 or abs(q - 1.20355) < 3e-3),
    ("250d", lambda q: abs(q - 1.00399) < 5e-4 or abs(q - 0.99602) < 5e-4),
    ("z1.96", lambda q: abs(q - 1.19158) < 2e-3),
    ("near_miss<0.2%", lambda q: abs(q - 1) < 2e-3),
]


def classify(value, ref):
    try:
        q = float(value) / float(ref)
    except (TypeError, ValueError, ZeroDivisionError):
        return "non_numeric"
    for name, test in PATTERNS:
        if test(q):
            return name
    return "other"


def first_failed_key(details):
    for k, d in details.items():
        if isinstance(d, dict) and d.get("ok") is False and "value" in d and \
                "reference" in d:
            return k, d
    # T3 wrong verdicts nest key details under 'keys'
    inner = details.get("keys")
    if isinstance(inner, dict):
        return first_failed_key(inner)
    return None, None


by_cond = defaultdict(Counter)
by_model_c1c3 = defaultdict(Counter)
examples = defaultdict(list)

for line in LOG.read_text(encoding="utf-8").splitlines():
    r = json.loads(line)
    if r["judge"]["bucket"] != "numeric_wrong":
        continue
    key, d = first_failed_key(r["judge"]["details"])
    if d is None:
        cls = "no_detail"
    else:
        cls = classify(d["value"], d["reference"])
    by_cond[r["condition"]][cls] += 1
    if r["condition"] in ("C1", "C3"):
        by_model_c1c3[r["model"]][cls] += 1
    if len(examples[cls]) < 3 and d is not None:
        examples[cls].append(
            f"{r['run_id']} {key}: {d['value']} vs ref {d['reference']}")

print("=== numeric_wrong failure classes by condition ===")
for cond in ("C1", "C2", "C3", "C4"):
    total = sum(by_cond[cond].values())
    print(f"\n{cond} (n={total}):")
    for cls, n in by_cond[cond].most_common():
        print(f"   {cls:16s} {n:4d}  ({100*n/max(total,1):.0f}%)")

print("\n=== C1+C3 failure classes by model ===")
for m in ("M1", "M2", "M3"):
    total = sum(by_model_c1c3[m].values())
    print(f"\n{m} (n={total}):")
    for cls, n in by_model_c1c3[m].most_common():
        print(f"   {cls:16s} {n:4d}")

print("\n=== examples per class ===")
for cls, exs in examples.items():
    print(f"\n[{cls}]")
    for e in exs:
        print("   " + e)

# no-code format failures by condition/model
print("\n=== no-code completions (format_failure without code) ===")
nc = Counter()
for line in LOG.read_text(encoding="utf-8").splitlines():
    r = json.loads(line)
    if r["judge"]["bucket"] == "format_failure" and not r["code_extracted"]:
        nc[(r["condition"], r["model"])] += 1
for (cond, m), n in sorted(nc.items()):
    print(f"   {cond} {m}: {n}")
