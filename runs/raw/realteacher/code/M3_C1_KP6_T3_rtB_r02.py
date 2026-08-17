import pandas as pd
import numpy as np

# 1. 读取你的课程数据文件（请根据实际文件格式和路径修改）
# df = pd.read_csv('你的课程数据文件.csv') 

# 2. 提取基金日收益列
# daily_returns = df['fund']

# --- 以下为计算核心逻辑（假设 daily_returns 已获取）---
rf_annual = 0.021
rf_daily = rf_annual / 252  # 将年化无风险利率转为日度

# 计算日收益的样本均值和样本标准差（ddof=1）
mean_daily = daily_returns.mean()
std_daily = daily_returns.std()

# 计算年化 Sharpe Ratio
# 公式: ((日均值 - 日无风险) / 日标准差) * sqrt(252)
sharpe_annual = ((mean_daily - rf_daily) / std_daily) * np.sqrt(252)

# 3. 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)
