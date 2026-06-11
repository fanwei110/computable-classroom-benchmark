"""Fig. 2 - Distribution of primary error classes by model, improvised
condition. Horizontal stacked bars, single-column width, Okabe-Ito palette
with hatching (color-blind and grayscale safe), n labels at bar ends.
Data: coding/auto/fig2_data.csv (final three-layer coding)."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "fig2_errors.pdf"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})

CLASSES = ["CV", "CN", "CD", "VZ"]
LABELS = {"CV": "Conventional", "CN": "Conceptual", "CD": "Code",
          "VZ": "Visualization"}
# Okabe-Ito, Convention darkest/leftmost per the figure spec
COLORS = {"CV": "#0072B2", "CN": "#E69F00", "CD": "#999999", "VZ": "#CC79A7"}
HATCH = {"CV": "", "CN": "//", "CD": "..", "VZ": "xx"}

df = pd.read_csv(ROOT / "coding" / "auto" / "fig2_data.csv")
MODELS = [("M3", "GLM-5.1"), ("M2", "DeepSeek-V4 Pro"), ("M1", "Mistral Large 2512")]

fig, ax = plt.subplots(figsize=(3.5, 2.1))
for yi, (m, label) in enumerate(MODELS):
    sub = df[df.model == m]
    n = len(sub)
    left = 0.0
    for c in CLASSES:
        share = (sub.final_class == c).mean() * 100 if n else 0
        ax.barh(yi, share, left=left, height=0.62, color=COLORS[c],
                hatch=HATCH[c], edgecolor="white", linewidth=0.4,
                label=LABELS[c] if yi == 0 else None)
        if share > 8:
            ax.text(left + share / 2, yi, f"{share:.0f}", ha="center",
                    va="center", fontsize=6.5,
                    color="white" if c == "CV" else "black")
        left += share
    ax.text(101.5, yi, f"n={n}", va="center", fontsize=6.5)

ax.set_yticks(range(len(MODELS)))
ax.set_yticklabels([lbl for _, lbl in MODELS], fontsize=7)
ax.set_xlabel("share of coded failures (%)", fontsize=7.5)
ax.set_xlim(0, 100)
ax.tick_params(axis="x", labelsize=7)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.32), ncol=4,
          fontsize=6.3, frameon=False, handlelength=1.2,
          columnspacing=0.9, handletextpad=0.4)

fig.savefig(OUT, bbox_inches="tight")
print(f"wrote {OUT}")
