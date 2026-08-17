import pandas as pd
import numpy as np

# 读取数据文件（请根据实际文件格式调整）
df = pd.read_csv('data.csv')

# 提取fund列的日收益率
daily_returns = df['fund']

# 参数
rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days

# 计算日收益率的均值和标准差
mean_daily = daily_returns.mean()
std_daily = daily_returns.std()

# 年化夏普比率 = (日均超额收益 / 日收益标准差) * sqrt(252)
sharpe_annual = (mean_daily - rf_daily) / std_daily * np.sqrt(trading_days)

# 输出契约
result = {'sharpe_annual': sharpe_annual}

print(f"年化夏普比率: {sharpe_annual:.4f}")
print(f"result = {result}")
