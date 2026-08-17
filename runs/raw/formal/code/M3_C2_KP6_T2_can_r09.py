#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
《证券投资学》课堂实时编程 —— 风险调整后业绩：滚动年化夏普比率
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ===================== 可调参数 =====================
WINDOW = 60          # 滚动窗口长度（交易日），可自行调整
ANNUAL_FACTOR = 252  # 年化交易日数
RF_ANNUAL = 0.021    # 年化无风险利率 2.1%

# ===================== 假设说明 =====================
# 1. 日无风险利率采用简单拆分：rf_daily = RF_ANNUAL / 252
# 2. 滚动标准差使用 ddof=1（样本标准差），与 pandas.rolling().std() 默认一致
# 3. 年化夏普 = (E[R_daily] - rf_daily) / σ_daily × sqrt(252)

# -------------------- Step 1: 读取数据 --------------------
csv_path = "data/market_snapshot_v1.csv"
df = pd.read_csv(csv_path)

# 提取 fund 列日收益率
daily_returns = df["fund"].astype(float)

# 日无风险利率
rf_daily = RF_ANNUAL / ANNUAL_FACTOR

# -------------------- Step 2: 滚动年化夏普 --------------------
rolling_mean = daily_returns.rolling(window=WINDOW).mean()
rolling_std = daily_returns.rolling(window=WINDOW).std()  # ddof=1 by default

rolling_sharpe = (rolling_mean - rf_daily) / rolling_std * np.sqrt(ANNUAL_FACTOR)

# -------------------- Step 3: 报告最后一个窗口 & 绘图 --------------------
# 最后一个有效窗口的夏普值
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# 绘图
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(rolling_sharpe.index, rolling_sharpe.values, linewidth=1.0, color="#1f77b4")
ax.axhline(y=0, color="grey", linestyle="--", linewidth=0.8)
ax.set_title(f"{WINDOW}-Day Rolling Annualized Sharpe Ratio (RF={RF_ANNUAL:.1%})", fontsize=13)
ax.set_xlabel("Trading Day Index", fontsize=11)
ax.set_ylabel("Annualized Sharpe Ratio", fontsize=11)
ax.grid(True, alpha=0.3)

# 标注最后一个值
ax.annotate(
    f"Last = {rolling_sharpe_last:.4f}",
    xy=(rolling_sharpe.index[-1], rolling_sharpe_last),
    xytext=(-120, 25),
    textcoords="offset points",
    fontsize=10,
    arrowprops=dict(arrowstyle="->", color="red"),
    color="red",
    fontweight="bold",
)

fig.tight_layout()

# -------------------- Step 4: 保存图形 & 填充 result --------------------
figure_path = "rolling_sharpe_ratio.png"
fig.savefig(figure_path, dpi=150)
plt.close(fig)

result = {
    "rolling_sharpe_last": float(rolling_sharpe_last),
    "figure_path": figure_path,
}

# 控制台输出，方便课堂投屏验证
print(f"Window length        : {WINDOW} days")
print(f"Annual risk-free rate: {RF_ANNUAL:.2%}")
print(f"Last rolling Sharpe  : {rolling_sharpe_last:.4f}")
print(f"Figure saved to      : {figure_path}")
