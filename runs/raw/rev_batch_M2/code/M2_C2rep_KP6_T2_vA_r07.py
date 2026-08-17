import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')          # 非交互式后端，保证保存图形时不弹出窗口
import matplotlib.pyplot as plt

# ============================
# 可调参数
# ============================
WINDOW = 60                    # 滚动窗口长度（交易日）
RISK_FREE_RATE_ANNUAL = 0.021 # 年化无风险利率
TRADING_DAYS_PER_YEAR = 252   # 每年交易日数
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'rolling_sharpe.png'

# ============================
# 1. 读取快照数据
# ============================
df = pd.read_csv(DATA_PATH)

# 自动识别日期列（如存在）
date_col = None
for col in df.columns:
    if 'date' in col.lower() or 'dt' in col.lower():
        date_col = col
        break
if date_col is not None:
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.set_index(date_col)
else:
    # 无日期列时保留整数索引，视为交易日序数
    pass

# 提取日收益率（假设为小数形式，例如 0.01 表示 1%）
fund_returns = df['fund'].astype(float)

# ============================
# 2. 计算日超额收益
# ============================
daily_risk_free = RISK_FREE_RATE_ANNUAL / TRADING_DAYS_PER_YEAR
daily_excess = fund_returns - daily_risk_free

# ============================
# 3. 定义年化夏普计算函数
# ============================
def annualized_sharpe(window_series: pd.Series) -> float:
    """传入窗口内的日超额收益序列，返回年化夏普比率"""
    if len(window_series) < 2:
        return np.nan
    mu = window_series.mean()
    sigma = window_series.std(ddof=1)   # 样本标准差
    if sigma == 0:
        return np.nan
    # 年化：均值*252 / (标准差*sqrt(252)) = 均值/标准差 * sqrt(252)
    return (mu / sigma) * np.sqrt(TRADING_DAYS_PER_YEAR)

# ============================
# 4. 计算滚动夏普
# ============================
rolling_sharpe = daily_excess.rolling(
    window=WINDOW,
    min_periods=WINDOW
).apply(annualized_sharpe, raw=False)

# ============================
# 5. 提取最后一个窗口的值
# ============================
last_value = rolling_sharpe.iloc[-1]
rolling_sharpe_last = float(last_value) if not pd.isna(last_value) else None

# ============================
# 6. 绘图并保存
# ============================
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.index, rolling_sharpe.values, linewidth=2)
plt.title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio', fontsize=14)
xlabel = 'Date' if date_col is not None else 'Trading Days'
plt.xlabel(xlabel)
plt.ylabel('Annualized Sharpe Ratio')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURE_PATH, dpi=150)
plt.close()

# ============================
# 7. 填充结果字典
# ============================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH
}

# 打印结果，便于课堂观察
print(result)
