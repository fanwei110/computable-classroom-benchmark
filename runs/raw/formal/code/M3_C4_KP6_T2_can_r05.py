import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ── 可调参数 ──
WINDOW = 60                     # 滚动窗口长度（交易日），可按需调整
ANNUAL_RF = 0.021               # 年化无风险利率（小数）
TRADING_DAYS = 252              # 每年交易日数

# ── 1. 读取数据 ──
df = pd.read_csv("data/market_snapshot_v1.csv")

# 取 fund 列日收益率
fund_daily = df["fund"]

# 日无风险利率
daily_rf = ANNUAL_RF / TRADING_DAYS

# ── 2. 滚动年化夏普比率 ──
excess_return = fund_daily - daily_rf

# 滚动均值与标准差（ddof=1）
rolling_mean = excess_return.rolling(window=WINDOW).mean()
rolling_std  = excess_return.rolling(window=WINDOW).std(ddof=1)

# 日夏普 → 年化夏普
rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS)

# ── 3. 报告最后一个窗口的夏普值 ──
rolling_sharpe_last = float(rolling_sharpe.iloc[-1])

# ── 4. 绘图 ──
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(rolling_sharpe.index, rolling_sharpe.values, linewidth=1.0, color="steelblue")
ax.axhline(0, color="grey", linewidth=0.5, linestyle="--")
ax.set_title(f"Rolling {WINDOW}-Day Annualized Sharpe Ratio (Fund)", fontsize=13)
ax.set_xlabel("Index")
ax.set_ylabel("Annualized Sharpe Ratio")
ax.grid(True, alpha=0.3)
fig.tight_layout()

figure_path = "rolling_sharpe.png"
fig.savefig(figure_path, dpi=150)
plt.close(fig)

# ── 输出契约 ──
result = {
    "rolling_sharpe_last": rolling_sharpe_last,
    "figure_path": figure_path,
}

print(result)
