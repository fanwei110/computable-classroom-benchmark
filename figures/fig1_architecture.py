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

FIG_W, FIG_H = 7.16, 4.05
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
# label pad: white box so labels stay readable over arrows (AE fix)
LB = dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.92)

box(0.8, 35.0, 19, 10.5,
    "Student question\n(instructor-mediated,\nnatural language)", fc="0.92", fs=7.0)
box(0.8, 15.0, 19, 13.0,
    "Router\n\n(in the\nCKU library?)")
arrow(10.3, 34.6, 10.3, 28.6)

box(0.8, 1.2, 19, 7.6,
    "CKU library\n(prefab CKU units)", fc="0.85", fs=6.9)
arrow(10.3, 15.0, 10.3, 9.4)

# ---- middle: two reliable layers + a hard boundary -------------------------
lx, lw_ = 26.5, 30
box(lx, 37.0, lw_, 8.6,
    "Layer 1: Prefabricated demo\n(verified CKU)",
    fc="0.90", weight="bold", fs=7.2)
box(lx, 23.0, lw_, 8.6,
    "Layer 2: In-library generation\n(via CKU template)",
    fc="0.95", weight="bold", fs=7.2)
# hard boundary of reliable live inquiry
ax.plot([29.0, lx + lw_ + 1.5], [20.0, 20.0], color="black",
        lw=1.1, linestyle=(0, (5, 2)))
ax.text(lx + lw_ - 1.0, 21.4, "perimeter of reliable live inquiry",
        fontsize=6.2, ha="right", style="italic", bbox=LB)
box(lx, 9.0, lw_, 8.6,
    "Out-of-library question\nno live demo; improvised\ngeneration is unreliable",
    fc="white", weight="bold", fs=6.9)

arrow(19.8, 25.5, lx - 0.5, 41.0)
arrow(19.8, 21.5, lx - 0.5, 27.3)
arrow(19.8, 17.5, lx - 0.5, 13.3)
# route labels: horizontal, offset from the arrows, on white pads (AE fix)
ax.text(22.8, 35.5, "anticipated", fontsize=6.2, ha="center", style="italic",
        bbox=LB)
ax.text(21.6, 22.2, "in-domain,\nunanticipated", fontsize=6.2, ha="center",
        style="italic", bbox=LB)
ax.text(16.5, 11.0, "out-of-library", fontsize=6.2, ha="center", style="italic",
        bbox=LB)

# library feeds layer 2 (dashed); self-explanatory ("via CKU template" is in
# the Layer-2 box), so no on-arrow label -- the corner was too crowded (AE fix)
arrow(19.8, 6.8, lx + 3.0, 22.6, ls=(0, (2, 2)), lw=0.8)
# out-of-library questions are harvested back into the library as new CKUs
arrow(lx + 3.5, 8.7, 20.2, 5.6, ls=(0, (2, 2)), lw=0.8)
ax.text(31.5, 3.0, "harvested as draft CKUs", fontsize=6.0, ha="center",
        style="italic", bbox=LB)

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
box(79.5, 22.0, 20, 17.5,
    "Instructor verification\n(two-stage)\n\n"
    "① Did it COMPUTE?\n(code, not constants)\n"
    "② Convention check\n(units, annualization)",
    fc="0.85", fs=6.4, weight="bold")
arrow(cx + cw + 0.5, 44.6, 88.0, 39.9)              # code -> verification
arrow(79.5, 26.5, cx + cw + 0.5, 31.5, ls=(0, (3, 2)))  # approve -> project
ax.text(86.5, 18.4, "approve / correct, then project", fontsize=6.2,
        ha="center", style="italic", bbox=LB)

fig.savefig(OUT, bbox_inches="tight")
fig.savefig(str(OUT).replace(".pdf", ".png"), dpi=220, bbox_inches="tight")
print(f"wrote {OUT} (+png)")
