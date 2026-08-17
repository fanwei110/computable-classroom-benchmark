import numpy as np
import pandas as pd

# 假设 df 是包含课程数据的 DataFrame，'fund' 列为日度收益率数据
# rf_annual 为年化无风险利率 2.1%
rf_annual = 0.021
rf_daily = rf_annual / 252  # 将年化无风险利率转换为日度

# 提取 fund 列的日度收益率数据
returns = df['fund']

# 计算日度平均超额收益
mean_excess_daily = returns.mean() - rf_daily

# 计算日度收益率的标准差（使用样本标准差，ddof=1）
std_daily = returns.std(ddof=1)

# 计算年化夏普比率
sharpe_annual = (mean_excess_daily / std_daily) * np.sqrt(252)

# 按照输出契约存入名为 result 的字典
result = {'sharpe_annual': sharpe_annual}

print(result)
