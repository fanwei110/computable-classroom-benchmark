import pandas as pd
import numpy as np

# 假设数据文件为 data.csv，有一列 'fund' 表示日收益率（小数形式，如 0.001 代表 0.1%）
# df = pd.read_csv('data.csv')
# daily_returns = df['fund']

# 若无数据，设 daily_returns 为空
daily_returns = pd.Series(dtype=float)

if daily_returns.empty:
    sharpe_annual = None
else:
    rf_annual = 0.021
    # 假设一年有252个交易日
    trading_days = 252
    rf_daily = (1 + rf_annual) ** (1/trading_days) - 1  # 更精确，或简化为 rf_annual/trading_days
    excess_daily = daily_returns - rf_daily
    mean_excess_daily = excess_daily.mean()
    std_daily = daily_returns.std()  # 夏普比率通常用收益率的波动，而非超额收益的波动，但常见是超额收益波动；这里使用收益率的波动，也可用超额收益波动，需保持一致
    # 若使用超额收益的标准差：std_excess_daily = excess_daily.std()
    # 年化夏普 = (年化平均超额收益) / (年化波动)
    # 年化平均超额 = mean_excess_daily * trading_days
    # 年化波动 = std_daily * np.sqrt(trading_days)
    annualized_excess_return = mean_excess_daily * trading_days
    annualized_vol = std_daily * np.sqrt(trading_days)
    sharpe_annual = annualized_excess_return / annualized_vol if annualized_vol != 0 else None

result = {'sharpe_annual': sharpe_annual}
