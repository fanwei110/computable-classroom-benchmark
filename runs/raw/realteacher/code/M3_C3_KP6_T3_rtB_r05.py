import numpy as np
import pandas as pd

# 假设数据框已加载为 df，基金日收益率列名为 'fund'
# df = pd.read_csv('你的课程数据文件.csv')

# 1. 设定参数
rf_annual = 0.021  # 无风险利率 2.1%
trading_days = 252 # 年化交易日

# 2. 将年化无风险利率（按年复利）转换为日无风险利率
rf_daily = (1 + rf_annual) ** (1 / trading_days) - 1

# 3. 计算日超额收益率
excess_daily = df['fund'] - rf_daily

# 4. 计算日超额收益率的均值与样本标准差(ddof=1)
mean_excess_daily = excess_daily.mean()
std_excess_daily = excess_daily.std(ddof=1)

# 5. 计算年化 Sharpe Ratio (日Sharpe * sqrt(252))
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(trading_days)

# 6. 按输出契约存入字典
result = {'sharpe_annual': sharpe_annual}
