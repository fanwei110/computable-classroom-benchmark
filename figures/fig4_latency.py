"""Fig.4 — latency and the truncation-cost tradeoff.
(A) per-condition distribution of end-to-end latency (median compatible with a
    classroom rhythm, but a long right tail);
(B) fraction of CORRECT generations discarded if an instructor truncates at t
    seconds — the cost is high precisely because slow generations tend to be
    right. Recomputed from runs/results_formal.csv. English labels (fig1-3 style).
"""
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "runs" / "results_formal.csv")
lat = "latency_total_s"
conds = ["C1", "C2", "C3", "C4"]
labels = {"C1": "C1\nimprovised", "C2": "C2\n+struct", "C3": "C3\n+conv", "C4": "C4\ntemplate"}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.2))

# (A) latency distribution by condition
data = [df[df.condition == c][lat].dropna().values for c in conds]
bp = ax1.boxplot(data, labels=[labels[c] for c in conds], showfliers=False,
                 patch_artist=True, medianprops=dict(color="black"))
for patch in bp["boxes"]:
    patch.set_facecolor("#a6cee3")
ax1.axhline(45, color="#922b21", ls="--", lw=1)
ax1.text(4.35, 46, "45 s", color="#922b21", fontsize=8, va="bottom", ha="right")
ax1.set_ylabel("End-to-end latency (s)", fontsize=11)
ax1.set_title("(A) Latency by condition", fontsize=11)
ax1.set_ylim(0, min(160, np.nanpercentile(df[lat], 97)))

# (B) fraction of CORRECT generations lost vs truncation cutoff
cutoffs = np.arange(0, 181, 1)
for c, col in [("C1", "#e31a1c"), ("C4", "#1f78b4"), ("ALL", "#555555")]:
    sub = df if c == "ALL" else df[df.condition == c]
    corr = sub[sub.correct == 1][lat].dropna().values
    if len(corr) == 0:
        continue
    lost = [np.mean(corr > t) for t in cutoffs]
    ax2.plot(cutoffs, np.array(lost) * 100, color=col, lw=1.8,
             label={"C1": "C1 improvised", "C4": "C4 template", "ALL": "all conditions"}[c])
for t in (45, 60):
    ax2.axvline(t, color="#922b21", ls=":", lw=1)
    ax2.text(t + 1, 92, f"{t}s", color="#922b21", fontsize=8)
ax2.set_xlabel("Instructor truncation cutoff (s)", fontsize=11)
ax2.set_ylabel("% of correct generations discarded", fontsize=11)
ax2.set_title("(B) Cost of a wait-then-fallback rule", fontsize=11)
ax2.set_xlim(0, 180); ax2.set_ylim(0, 100)
ax2.legend(fontsize=9, loc="upper right")

fig.tight_layout()
fig.savefig(ROOT / "figures" / "fig4_latency.pdf", bbox_inches="tight")
fig.savefig(ROOT / "figures" / "fig4_latency.png", dpi=200, bbox_inches="tight")
med = df.groupby("condition")[lat].median()
print("wrote fig4_latency.pdf/.png ; medians:",
      {c: round(float(med[c]), 1) for c in conds})
corrall = df[df.correct == 1][lat].dropna().values
print(f"lost@45s(all correct) = {100*np.mean(corrall>45):.1f}%  lost@60s = {100*np.mean(corrall>60):.1f}%")
