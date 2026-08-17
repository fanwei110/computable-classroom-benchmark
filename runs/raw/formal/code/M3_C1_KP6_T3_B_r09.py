import numpy as np
import pandas as pd

# 假设 df 为包含基金数据的 DataFrame，'fund' 列为日度收益率
# rf = 2.1%
rf_annual = 0.021

# 将年化无风险利率转换为日度无风险利率（假设一年252个交易日）
rf_daily = (1 + rf_annual) ** (1/252) - 1

# 计算 fund 列全样本的日超额收益率
excess_returns = df['fund'] - rf_daily

# 计算年化夏普比率：(日均超额收益 / 日超额收益标准差) * sqrt(252)
sharpe_annual = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}
