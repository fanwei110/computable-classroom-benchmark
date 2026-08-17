import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------ 参数 ------------------------------
WINDOW = 60                  # 滚动窗口长度（可调）
RF_ANNUAL = 0.021            # 年化无风险利率
TRADING_DAYS = 252           # 一年中的交易日数
DATA_PATH = "data/market_snapshot_v1.csv"
FIGURE_PATH = "rolling_sharpe.png"

# ------------------------------ 1. 读取数据 ------------------------------
# 假设 CSV 包含 'date' 和 'fund' 列，'fund' 为小数形式的日收益率
df = pd.read_csv(DATA_PATH, parse_dates=['date'], index_col='date')
fund_ret = df['fund']  # 日收益序列

# ------------------------------ 2. 计算超额收益 ------------------------------
rf_daily = RF_ANNUAL / TRADING_DAYS          # 日化无风险利率
excess_ret = fund_ret - rf_daily             # 日超额收益

# ------------------------------ 3. 计算滚动年化夏普比率 ------------------------------
def annualized_sharpe(series: np.ndarray) -> float:
    """由日超额收益的 numpy 数组计算年化夏普比率"""
    # 如果标准差为零，返回 np.nan 以避免除零错误
    std = np.std(series, ddof=1)   # 样本标准差
    if std == 0:
        return np.nan
    return np.sqrt(TRADING_DAYS) * np.mean(series) / std

rolling_sharpe = (
    excess_ret
    .rolling(window=WINDOW, min_periods=WINDOW)
    .apply(annualized_sharpe, raw=True)
    .dropna()
)

# ------------------------------ 4. 报告最后一个窗口的值 ------------------------------
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# ------------------------------ 5. 画图并保存 ------------------------------
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(rolling_sharpe.index, rolling_sharpe.values, color='darkblue', linewidth=1.0)
ax.set_title(f"{WINDOW}-Day Rolling Annualized Sharpe Ratio (Fund)", fontsize=14)
ax.set_xlabel("Date")
ax.set_ylabel("Annualized Sharpe Ratio")
ax.grid(True, linestyle='--', alpha=0.6)
ax.axhline(0, color='black', linewidth=0.8)
fig.tight_layout()
fig.savefig(FIGURE_PATH, dpi=150)
plt.close(fig)

# ------------------------------ 6. 填充结果字典 ------------------------------
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH,
}

# 若在交互环境中直接检查，可取消下一行的注释
# print(result)
