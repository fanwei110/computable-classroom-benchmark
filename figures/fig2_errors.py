"""Fig. 2 - Mechanically determined composition of improvised (C1) failures.
Deliberately does NOT use the conventional/conceptual split, which the human
audit found unreliable (inter-coder kappa 0.03). Uses only the mechanical
`bucket` field + the deterministic hard-coded-constant flag:
  no-code/contract (format_failure) | code crashed (code_error) |
  silent-executed-wrong (numeric_wrong; hard-coded const split out) | visualization.
Data: runs/results_formal.csv + coding/auto/final_coded.csv (hardcoded flag).
Horizontal stacked bars by model, Okabe-Ito palette, color-blind/grayscale safe."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "fig2_errors.pdf"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})

df = pd.read_csv(ROOT / "runs" / "results_formal.csv")
fc = pd.read_csv(ROOT / "coding" / "auto" / "final_coded.csv")[["run_id", "hardcoded"]]
c1 = df[(df.condition == "C1") & (df.correct == 0)].merge(fc, on="run_id", how="left")

def cat(r):
    if r.bucket == "format_failure":
        return "nocode"
    if r.bucket == "code_error":
        return "crash"
    if r.bucket == "vis_failure":
        return "vis"
    if r.bucket == "numeric_wrong":
        return "silent_hc" if r.hardcoded == 1 else "silent_other"
    return "other"

c1 = c1.assign(cat=c1.apply(cat, axis=1))

CATS = ["nocode", "crash", "silent_hc", "silent_other", "vis"]
LAB = {"nocode": "No-code / contract", "crash": "Code crashed",
       "silent_hc": "Silent: hard-coded const", "silent_other": "Silent: other wrong",
       "vis": "Visualization"}
COL = {"nocode": "#56B4E9", "crash": "#0072B2", "silent_hc": "#D55E00",
       "silent_other": "#E69F00", "vis": "#CC79A7"}
HAT = {"nocode": "", "crash": "//", "silent_hc": "xx", "silent_other": "..", "vis": "\\\\"}
MODELS = [("M3", "GLM-5.1"), ("M2", "DeepSeek-V4 Pro"), ("M1", "Mistral Large 2512")]

fig, ax = plt.subplots(figsize=(3.7, 2.2))
for yi, (m, label) in enumerate(MODELS):
    sub = c1[c1.model == m]
    n = len(sub); left = 0.0
    for c in CATS:
        share = (sub.cat == c).mean() * 100 if n else 0
        ax.barh(yi, share, left=left, height=0.62, color=COL[c], hatch=HAT[c],
                edgecolor="white", linewidth=0.4, label=LAB[c] if yi == 0 else None)
        if share > 7:
            # black text on a small white pad: readable on any fill/hatch (AE fix)
            ax.text(left + share / 2, yi, f"{share:.0f}", ha="center", va="center",
                    fontsize=6.5, color="black",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none",
                              alpha=0.9))
        left += share
    ax.text(101.5, yi, f"n={n}", va="center", fontsize=6.5)

ax.set_yticks(range(len(MODELS)))
ax.set_yticklabels([l for _, l in MODELS], fontsize=7)
ax.set_xlabel("share of improvised (C1) failures (%)", fontsize=7.5)
ax.set_xlim(0, 100)
ax.tick_params(axis="x", labelsize=7)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.42), ncol=2, fontsize=6.0,
          frameon=False, handlelength=1.2, columnspacing=0.9, handletextpad=0.4)

fig.savefig(OUT, bbox_inches="tight")
fig.savefig(str(OUT).replace(".pdf", ".png"), dpi=200, bbox_inches="tight")
tot = c1.cat.value_counts().to_dict()
vis_ = tot.get("nocode", 0) + tot.get("crash", 0)
sil = tot.get("silent_hc", 0) + tot.get("silent_other", 0)
print(f"wrote {OUT.name} ; total C1 failures={len(c1)} | counts={tot}")
print(f"visible(nocode+crash)={vis_}  silent(hc+other)={sil}  hard-coded={tot.get('silent_hc',0)}")
