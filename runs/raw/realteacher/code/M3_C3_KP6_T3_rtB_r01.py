import pandas as pd
import numpy as np

# 1. 读取数据文件（请根据实际文件格式调整，如 pd.read_excel('xxx.xlsx')）
df = pd.read_csv('你的课程数据文件.csv') 

# 2. 提取基金日收益列
daily_returns = df['fund']

# 3. 设定无风险利率（按约定使用小数 0.021 表示 2.1%）
rf_annual = 0.021

# 计算每日无风险利率（常规做法：年化单利转为日度单利）
rf_daily = rf_annual / 252

# 4. 计算日超额收益的均值
mean_excess_daily = daily_returns.mean() - rf_daily

# 5. 计算日收益的样本标准差（严格按约定 ddof=1）
std_daily = daily_returns.std(ddof=1)

# 6. 计算年化 Sharpe ratio
# 年化超额收益 = mean_excess_daily * 252
# 年化标准差 = std_daily * sqrt(252)
# 年化 Sharpe = (mean_excess_daily * 252) / (std_daily * sqrt(252)) 
#             = (mean_excess_daily / std_daily) * sqrt(252)
sharpe_annual = (mean_excess_daily / std_daily) * np.sqrt(252)

# 7. 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

# 输出结果
print(result)
