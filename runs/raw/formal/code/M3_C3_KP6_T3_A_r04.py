import pandas as pd
import numpy as np

# 假设课程数据已加载为 DataFrame，名为 df
# 计算基金的日简单收益率（剔除首日空值）
daily_returns = df['fund'].pct_change().dropna()

# 无风险利率（小数表示）
rf_annual = 0.021

# 1. 计算年化收益率（算术平均，按252个交易日年化）
annual_return = daily_returns.mean() * 252

# 2. 计算年化波动率（样本标准差 ddof=1，按252个交易日年化）
annual_volatility = daily_returns.std(ddof=1) * np.sqrt(252)

# 3. 计算年化夏普比率
sharpe_annual = (annual_return - rf_annual) / annual_volatility

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}
