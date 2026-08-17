import pandas as pd
import numpy as np

# ================= 假设读取数据 =================
# df = pd.read_csv('your_data_file.csv') # 请根据实际文件格式读取
# daily_returns = df['fund']             # 提取fund列的日收益
# =================================================

# 参数设定
rf_annual = 0.021          # 年化无风险利率 2.1%
trading_days = 252         # 一年的交易日天数（中国市场一般取242或252，此处以252为例）

# 1. 计算日无风险利率（单利折算，行业通用做法）
rf_daily = rf_annual / trading_days

# 2. 计算整个样本期的日超额收益
# 注意：此计算假设fund列的日收益率为小数格式（如0.01表示1%），若为百分数需先除以100
excess_daily_returns = daily_returns - rf_daily

# 3. 计算整个样本期的日超额收益均值与标准差（使用样本标准差 ddof=1）
mean_excess = excess_daily_returns.mean()
std_excess = excess_daily_returns.std(ddof=1)

# 4. 计算年化夏普比率
sharpe_daily = mean_excess / std_excess
sharpe_annual = sharpe_daily * np.sqrt(trading_days)

# 5. 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}

print(result)
