import pandas as pd
import numpy as np

# 假设数据文件已读取为 DataFrame，名为 df
# df = pd.read_csv('your_data_file.csv') 

# 提取 fund 列的日收益率
daily_returns = df['fund']

# 无风险年化利率（小数表示）
rf_annual = 0.021

# 计算日无风险利率（非期权，按每年252个交易日直接拆分）
rf_daily = rf_annual / 252

# 计算日超额收益均值
mean_excess_daily = daily_returns.mean() - rf_daily

# 计算日收益率的样本标准差（ddof=1）
std_daily = daily_returns.std(ddof=1)

# 计算年化夏普比率
# 年化方式：均值乘以252，标准差乘以根号252，合并即为乘以根号252
sharpe_annual = (mean_excess_daily / std_daily) * np.sqrt(252)

# 按照输出契约存入字典
result = {
    'sharpe_annual': sharpe_annual
}
