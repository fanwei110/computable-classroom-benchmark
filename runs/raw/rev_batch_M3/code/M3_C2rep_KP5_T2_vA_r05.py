#!/usr/bin/env python3
"""
证券投资学课堂演示：历史VaR计算与损益分布可视化
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ============================================================
# 可调参数
# ============================================================
CONFIDENCE_LEVEL = 0.95          # 置信水平，可改为 0.99 等
POSITION         = 1_000_000    # 头寸（人民币）
DATA_PATH        = "data/market_snapshot_v1.csv"
FIGURE_PATH      = "daily_pnl_var_histogram.png"

# ============================================================
# 1. 读取快照 CSV，构造头寸的日损益
# ============================================================
df = pd.read_csv(DATA_PATH)

# 取 fund 列日收益率，去除缺失值
daily_returns = df["fund"].dropna().values

# 日损益 = 头寸 × 日收益率
daily_pnl = POSITION * daily_returns

# ============================================================
# 2. 由经验分布计算历史 VaR（人民币）
# ============================================================
# VaR 在 (1 - confidence) 分位数上取值，取负号报告为正数
alpha_frac = 1.0 - CONFIDENCE_LEVEL                       # 如 0.05
pnl_quantile = np.percentile(daily_pnl, alpha_frac * 100)  # 5% 分位数，通常为负
hist_var = -pnl_quantile                                   # 报告为正数（损失额）

# ============================================================
# 3. 画直方图并加带标注的 VaR 线
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))

# 直方图
n_bins = 50
counts, bin_edges, patches = ax.hist(
    daily_pnl,
    bins=n_bins,
    color="steelblue",
    edgecolor="white",
    alpha=0.85,
    label="日损益分布",
)

# VaR 竖线（画在 P&L 分位数处，即负值位置）
ax.axvline(
    x=pnl_quantile,
    color="red",
    linestyle="--",
    linewidth=2,
    label=(
        f"{CONFIDENCE_LEVEL*100:.0f}% 1日历史VaR\n"
        f"分位数 = ¥{pnl_quantile:,.2f}\n"
        f"VaR = ¥{hist_var:,.2f}"
    ),
)

# 在线旁加文字标注
y_top = ax.get_ylim()[1]
ax.annotate(
    f"VaR = ¥{hist_var:,.0f}",
    xy=(pnl_quantile, y_top * 0.55),
    xytext=(pnl_quantile + (bin_edges[-1] - bin_edges[0]) * 0.18, y_top * 0.65),
    fontsize=12,
    color="red",
    fontweight="bold",
    arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
)

# 坐标轴与标题
ax.set_title(
    f"日损益分布与历史VaR  "
    f"(头寸 ¥{POSITION/1e4:.0f}万, 置信水平 {CONFIDENCE_LEVEL*100:.0f}%)",
    fontsize=14,
    fontweight="bold",
)
ax.set_xlabel("日损益 (人民币)", fontsize=12)
ax.set_ylabel("频数", fontsize=12)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"¥{x:,.0f}"))
ax.legend(loc="upper left", fontsize=10, framealpha=0.9)
ax.grid(axis="y", alpha=0.3)

fig.tight_layout()

# ============================================================
# 4. 保存图形并填充 result
# ============================================================
fig.savefig(FIGURE_PATH, dpi=150, bbox_inches="tight")
plt.close(fig)

result = {
    "hist_var_95_1d": round(float(hist_var), 2),
    "figure_path": FIGURE_PATH,
}

# ---- 课堂打印（方便投屏确认）----
print("=" * 55)
print(f"  置信水平          : {CONFIDENCE_LEVEL*100:.0f}%")
print(f"  头寸              : ¥{POSITION:>12,}")
print(f"  1日历史VaR (95%)  : ¥{hist_var:>12,.2f}")
print(f"  图形已保存至      : {FIGURE_PATH}")
print("=" * 55)
