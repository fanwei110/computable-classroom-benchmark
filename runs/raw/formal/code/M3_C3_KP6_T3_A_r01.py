import pandas as pd
import numpy as np

# 假设您的数据已加载为 df，且包含 'fund' 列
# df = pd.read_csv('your_course_data.csv')

# 提取基金日收益率序列（假设已经是收益率，若是净值需先 .pct_change().dropna()）
r = df['fund']

# 1. 计算日收益率均值
mu = r.mean()

# 2. 计算日收益率样本标准差 (ddof=1)
sigma = r.std(ddof=1)

# 3. 计算日无风险利率 (年复利报价2.1%，每年252个交易日)
Rf_annual = 0.021
Rf_daily = (1 + Rf_annual) ** (1 / 252) - 1

# 4. 计算年化夏普比率
sharpe_annual = (mu - Rf_daily) / sigma * np.sqrt(252)

# 按输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)
