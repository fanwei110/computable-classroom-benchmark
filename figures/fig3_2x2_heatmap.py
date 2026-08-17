"""Fig.3 — 2x2 correctness heatmap: the headline at a glance.
Rows = structural scaffolding (top: +structure, bottom: -structure),
cols = convention information (left: -conv, right: +conv).
Shows correctness JUMPS along the structure axis but is ~FLAT along the
convention axis at the bottom row (the interaction). Numbers recomputed from
runs/results_formal.csv so the figure matches the text exactly.
English labels (consistent with fig1/fig2 and the English submission).
"""
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "runs" / "results_formal.csv")
ru = df.groupby("condition").correct.mean() * 100          # unrounded (for deltas)
r = ru.round(1)                                              # rounded (for cell display)
C1, C2, C3, C4 = r["C1"], r["C2"], r["C3"], r["C4"]
dC2C1, dC4C3 = ru["C2"] - ru["C1"], ru["C4"] - ru["C3"]     # structure deltas
dC3C1, dC4C2 = ru["C3"] - ru["C1"], ru["C4"] - ru["C2"]     # convention deltas

# grid[row][col]: row0 = +structure (top), row1 = -structure (bottom)
grid = np.array([[C2, C4], [C1, C3]])
names = np.array([["C2", "C4"], ["C1", "C3"]])

plt.rcParams.update({"font.family": "DejaVu Sans"})
fig, ax = plt.subplots(figsize=(5.7, 5.0))
im = ax.imshow(grid, cmap="YlGnBu", vmin=0, vmax=100, aspect="equal")

ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
ax.set_xticklabels(["No convention\nhint", "Convention\nhint"], fontsize=11)
ax.set_yticklabels(["+ Structure\n(CKU scaffold)", "- Structure\n(improvised)"], fontsize=11)
ax.set_xlabel("Convention information", fontsize=12, labelpad=8)
ax.set_ylabel("Structural scaffolding", fontsize=12, labelpad=8)

for i in range(2):
    for j in range(2):
        val = grid[i, j]
        tc = "white" if val > 55 else "black"
        ax.text(j, i, f"{names[i,j]}\n{val:.1f}%", ha="center", va="center",
                color=tc, fontsize=15, fontweight="bold")

# delta annotations: structure axis (vertical) jumps; convention axis (horizontal) ~flat at bottom
# white pads behind every annotation so the rotated text never sits on colored cells (AE fix)
BOX = dict(boxstyle="round,pad=0.25", fc="white", ec="0.55", lw=0.6, alpha=0.95)
ax.annotate(f"structure\n+{dC2C1:.1f} pp", xy=(-0.40, 0.5), xycoords=("data", "data"),
            ha="center", va="center", rotation=90, fontsize=10.5, fontweight="bold",
            color="#1a5276", bbox=BOX)
ax.annotate(f"structure\n+{dC4C3:.1f} pp", xy=(1.40, 0.5), xycoords=("data", "data"),
            ha="center", va="center", rotation=90, fontsize=10.5, fontweight="bold",
            color="#1a5276", bbox=BOX)
ax.annotate(f"convention +{dC3C1:.1f} pp", xy=(0.5, 1.42), xycoords=("data", "data"),
            ha="center", va="center", fontsize=10.5, fontweight="bold",
            color="#922b21", bbox=BOX)
ax.annotate(f"convention +{dC4C2:.1f} pp", xy=(0.5, -0.42), xycoords=("data", "data"),
            ha="center", va="center", fontsize=10.5, fontweight="bold",
            color="#922b21", bbox=BOX)

ax.set_xlim(-0.6, 1.6); ax.set_ylim(1.6, -0.6)
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.10)
cbar.set_label("Strict numerical correctness (%)", fontsize=11)
cbar.ax.tick_params(labelsize=10)
fig.tight_layout()
fig.savefig(ROOT / "figures" / "fig3_2x2_heatmap.pdf", bbox_inches="tight")
fig.savefig(ROOT / "figures" / "fig3_2x2_heatmap.png", dpi=200, bbox_inches="tight")
print(f"wrote fig3_2x2_heatmap.pdf/.png ; cells C1={C1} C2={C2} C3={C3} C4={C4}")
print(f"structure deltas: C2-C1=+{C2-C1:.1f}, C4-C3=+{C4-C3:.1f} | "
      f"convention deltas: C3-C1=+{C3-C1:.1f}, C4-C2=+{C4-C2:.1f}")
