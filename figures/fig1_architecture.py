"""Fig. 1 - Architecture of the computable classroom and CKU pipeline.

Vector PDF, two-column width (7.16 in), grayscale only, fonts >= 6.5 pt.
Three deployment layers (prefabricated / in-library templated /
out-of-library + convention header), the classroom four-stage chain, and
the instructor verification loop with the 4-question checklist.
Contains no data and no expected numbers (preregistration hygiene).
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent / "fig1_architecture.pdf"

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.5})

FIG_W, FIG_H = 7.16, 3.55
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.set_xlim(0, 100)
ax.set_ylim(0, 50)
ax.axis("off")


def box(x, y, w, h, text, fc="white", fs=7.2, weight="normal", lw=0.9):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.35", fc=fc,
                       ec="black", lw=lw)
    ax.add_patch(p)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, weight=weight, linespacing=1.25)


def arrow(x1, y1, x2, y2, lw=0.9, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", lw=lw,
                                 linestyle=ls, color="black", mutation_scale=8))


# ---- left: question entry + router + library ------------------------------
box(1.5, 35.0, 16.5, 10.5,
    "Student question\n(instructor-mediated,\nnatural language)", fc="0.92")
box(1.5, 15.0, 16.5, 13.0,
    "Router\nin the CKU library?\nwithin a unit's\ndomain?")
arrow(9.75, 34.6, 9.75, 28.6)

box(1.5, 1.2, 16.5, 7.6,
    "CKU library\nconcept card | ref. impl.\nvis. spec | template", fc="0.85", fs=6.6)
arrow(9.75, 15.0, 9.75, 9.4)

# ---- middle: two reliable layers + a hard boundary -------------------------
lx, lw_ = 26.5, 30
box(lx, 37.0, lw_, 8.6,
    "Layer 1 - Prefabricated demo\nverified CKU, ground-truth checked",
    fc="0.90", weight="bold", fs=7.0)
box(lx, 23.0, lw_, 8.6,
    "Layer 2 - In-library generation\nthrough the CKU prompt template",
    fc="0.95", weight="bold", fs=7.0)
# hard boundary of reliable live inquiry
ax.plot([lx - 1.5, lx + lw_ + 1.5], [20.0, 20.0], color="black",
        lw=1.1, linestyle=(0, (5, 2)))
ax.text(lx + lw_ / 2, 21.0, "perimeter of reliable live inquiry",
        fontsize=6.2, ha="center", style="italic")
box(lx, 9.0, lw_, 8.6,
    "Out-of-library question\nno live demo - improvised generation\n"
    "is unreliable and a convention header\ndoes not rescue it",
    fc="white", weight="bold", fs=6.4)

arrow(18.4, 25.5, lx - 0.5, 41.0)
arrow(18.4, 21.5, lx - 0.5, 27.3)
arrow(18.4, 17.5, lx - 0.5, 13.3)
ax.text(21.2, 34.2, "anticipated", fontsize=6.2, ha="center", style="italic",
        rotation=44)
ax.text(22.4, 25.6, "in-domain,\nunanticipated", fontsize=6.2, ha="center",
        style="italic", rotation=14)
ax.text(21.8, 14.0, "out-of-library", fontsize=6.2, ha="center", style="italic",
        rotation=-13)

# library feeds layers 1 and 2 (dashed)
arrow(18.4, 6.8, lx + 3.0, 22.6, ls=(0, (2, 2)), lw=0.8)
ax.text(20.0, 8.6, "templates,\nverified units", fontsize=6.0, ha="center",
        style="italic")
# out-of-library questions are harvested back into the library as new CKUs
arrow(lx + 6.0, 8.6, 14.0, 5.2, ls=(0, (2, 2)), lw=0.8)
ax.text(24.0, 3.6, "harvested as draft CKUs", fontsize=6.0, ha="center",
        style="italic")

# ---- right: classroom chain -------------------------------------------------
cx, cw = 62.0, 15
chain = [("Runnable code", 40.0), ("Dynamic\nvisualization", 29.0),
         ("Interactive\nexperimentation", 18.0), ("Reflective\ninterpretation", 7.0)]
for label, cy in chain:
    box(cx, cy, cw, 7.6, label, fc="0.92", fs=7.0)
for i in range(len(chain) - 1):
    arrow(cx + cw / 2, chain[i][1] - 0.4, cx + cw / 2, chain[i + 1][1] + 8.0)

# only the two reliable layers feed the classroom chain
arrow(lx + lw_ + 0.5, 41.5, cx - 0.5, 45.2)
arrow(lx + lw_ + 0.5, 27.3, cx - 0.5, 43.4)

# ---- instructor verification loop --------------------------------------------
box(80.0, 22.0, 19, 17.5,
    "Instructor verification\ntwo-stage check\n"
    "1  did it COMPUTE?\n(code, not constants)\n"
    "2  convention spot-check\n(units, annualization,\nestimator details)",
    fc="0.85", fs=6.3, weight="bold")
arrow(cx + cw + 0.5, 44.6, 88.0, 39.9)              # code -> verification
arrow(79.5, 26.5, cx + cw + 0.5, 31.5, ls=(0, (3, 2)))  # approve -> project
ax.text(89.0, 18.6, "approve / correct, then project", fontsize=6.2,
        ha="center", style="italic")

fig.savefig(OUT, bbox_inches="tight")
print(f"wrote {OUT}")
