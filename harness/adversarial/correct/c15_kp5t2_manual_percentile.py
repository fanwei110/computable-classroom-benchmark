# Correct T2 solution computing the empirical percentile BY HAND with the
# same linear interpolation as numpy's default (must be judged correct).
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

position = 1_000_000.0
conf = 0.95

df = pd.read_csv("data/market_snapshot_v1.csv")
pnl = sorted(x * position for x in df["fund"])

q = (1 - conf) * (len(pnl) - 1)
lo = int(math.floor(q))
frac = q - lo
quantile = pnl[lo] + frac * (pnl[lo + 1] - pnl[lo])
var95 = -quantile

os.makedirs("harness/_tmp", exist_ok=True)
fig, ax = plt.subplots()
ax.hist(pnl, bins=40)
ax.axvline(quantile, color="k", linestyle="--", label=f"95% VaR = {var95:,.0f}")
ax.set_xlabel("daily P&L (CNY)"); ax.legend()
path = "harness/_tmp/c15_var_hist.png"
fig.savefig(path, dpi=100)
plt.close(fig)

result = {"hist_var_95_1d": var95, "figure_path": path}
