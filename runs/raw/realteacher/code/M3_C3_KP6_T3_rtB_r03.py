import pandas as pd
import numpy as np

# 1. 读取数据（请根据实际文件格式修改，如 pd.read_excel）
df = pd.read_csv('你的课程数据文件.csv')  

# 2. 提取基金日收益列
daily_returns = df['fund']

# 3. 设定无风险利率并转为日度
rf_annual = 0.021
rf_daily = rf_annual / 252

# 4. 计算日超额收益
excess_daily_returns = daily_returns - rf_daily

# 5. 计算均值和样本标准差 (ddof=1 符合计算约定)
mean_excess = excess_daily_returns.mean()
std_excess = excess_daily_returns.std(ddof=1)

# 6. 计算日夏普比率并年化
sharpe_daily = mean_excess / std_excess
sharpe_annual = sharpe_daily * np.sqrt(252)

# 7. 按输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

# 打印结果查看
print(result)
