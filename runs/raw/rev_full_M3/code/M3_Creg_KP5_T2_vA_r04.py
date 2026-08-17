#!/usr/bin/env python3
"""
日损益分布直方图 & 95% 一日历史 VaR 计算
─────────────────────────────────────────
读取课程数据快照中 'fund' 列的日收益序列，
对 1,000,000 元头寸计算日损益并画直方图，
用带标注的竖线标出指定置信水平的一日历史 VaR。
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")                       # 无头后端，确保服务器可运行
import matplotlib.pyplot as plt

# ================================================================
# 可调参数
# ================================================================
CONFIDENCE_LEVEL = 0.95          # 置信水平，可改为 0.90 / 0.99 等
POSITION         = 1_000_000    # 头寸（人民币）
DATA_FILE        = "fund_data.csv"   # 课程数据快照路径

# ================================================================
# 1. 读取课程数据快照
# ================================================================
df = pd.read_csv(DATA_FILE)
# 取 'fund' 列，去缺失，确保 float
daily_returns = df["fund"].dropna().values.astype(float)

# ================================================================
# 2. 计算日损益序列 & 历史分位数 VaR
# ================================================================
daily_pnl = daily_returns * POSITION          # 日损益（人民币）
alpha     = 1 - CONFIDENCE_LEVEL              # 显著性水平

# 历史 VaR：P&L 分布的 alpha 分位数取负号（正数代表可能损失）
pnl_at_var = np.percentile(daily_pnl, alpha * 100)   # alpha 分位数 P&L
hist_var   = -pnl_at_var                               # VaR（正数）

# ================================================================
# 3. 画日损益分布直方图 + VaR 竖线
# ================================================================
fig, ax = plt.subplots(figsize=(10, 6))

# 直方图
ax.hist(
    daily_pnl,
    bins=50,
    edgecolor="black",
    alpha=0.70,
    color="steelblue",
    label=f"Daily P&L  (n = {len(daily_pnl)})",
)

# 零线
ax.axvline(0, color="grey", linewidth=0.8, linestyle="-")

# VaR 竖线
ax.axvline(
    pnl_at_var,
    color="red",
    linestyle="--",
    linewidth=2,
    label=(
        f"{CONFIDENCE_LEVEL * 100:.0f}% 1‑day Hist VaR = "
        f"¥{hist_var:,.0f}"
    ),
)

# 在竖线旁加标注文字
ylim_top = ax.get_ylim()[1]
ax.annotate(
    f"VaR\n¥{hist_var:,.0f}",
    xy=(pnl_at_var, ylim_top * 0.75),
    fontsize=10,
    fontweight="bold",
    color="red",
    ha="right" if pnl_at_var < 0 else "left",
    va="top",
)

ax.set_xlabel("Daily P&L (RMB)", fontsize=12)
ax.set_ylabel("Frequency", fontsize=12)
ax.set_title(
    f"Daily P&L Distribution  |  Position = ¥{POSITION:,}  |  "
    f"Confidence = {CONFIDENCE_LEVEL * 100:.0f}%",
    fontsize=13,
)
ax.legend(fontsize=11, loc="upper left")
fig.tight_layout()

figure_path = "daily_pnl_var_histogram.png"
fig.savefig(figure_path, dpi=150, bbox_inches="tight")
plt.close(fig)

# ================================================================
# 4. 输出
# ================================================================
print(f"{CONFIDENCE_LEVEL * 100:.0f}% 1-day Historical VaR = ¥{hist_var:,.2f}")

result = {
    "hist_var_95_1d": hist_var,
    "figure_path": figure_path,
}

print(result)
