import numpy as np
import pandas as pd

# 示例数据（假设 df 已加载）
# df = pd.read_csv('课程数据文件.csv')  # 实际应用中需替换为读取文件
daily_returns = df['fund']  # 基金日收益

# 无风险利率（年化 2.1%，转换为日收益）
rf_annual = 0.021
rf_daily = rf_annual / 252

# 计算日超额收益
excess_returns = daily_returns - rf_daily

# 计算超额收益的均值和标准差（样本估计量）
mu_excess = excess_returns.mean()
sigma_excess = excess_returns.std(ddof=1)

# 年化夏普比率
sharpe_annual = (mu_excess * np.sqrt(252)) / sigma_excess

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
