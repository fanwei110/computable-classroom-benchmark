import numpy as np
import pandas as pd

# 假设你的课程数据已经加载为 DataFrame df，且包含 'fund' 列
# 注意：以下代码假设 df['fund'] 已经是日收益率数据。
# 如果 'fund' 是净值数据，请先运行：df['fund'] = df['fund'].pct_change().dropna()

rf_annual = 0.021  # 年化无风险利率 2.1%
trading_days = 252 # 一年的交易日

# 计算日无风险利率
rf_daily = rf_annual / trading_days

# 计算每日超额收益率
excess_returns = df['fund'] - rf_daily

# 计算年化夏普比率：(日均超额收益 / 日超额收益标准差) * sqrt(252)
sharpe_daily = excess_returns.mean() / excess_returns.std()
sharpe_annual = sharpe_daily * np.sqrt(trading_days)

# 按输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)
