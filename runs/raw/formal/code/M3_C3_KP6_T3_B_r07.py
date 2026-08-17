import numpy as np
import pandas as pd

# 假设 fund 是包含全样本日收益率（小数表示）的 pandas Series
# fund = pd.Series([...]) 

rf = 0.021  # 2.1% 用小数表示
trading_days = 252

# 1. 计算日超额收益率
daily_excess_return = fund - (rf / trading_days)

# 2. 计算年化超额收益（算术平均年化）
annualized_excess_return = daily_excess_return.mean() * trading_days

# 3. 计算年化波动率（样本标准差 ddof=1，乘以 sqrt(252) 年化）
annualized_vol = fund.std(ddof=1) * np.sqrt(trading_days)

# 4. 计算年化夏普比率
sharpe_annual = annualized_excess_return / annualized_vol

# 5. 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)
