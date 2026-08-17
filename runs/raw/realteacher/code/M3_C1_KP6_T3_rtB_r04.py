import pandas as pd
import numpy as np

# 1. 读取你的课程数据文件 (请根据实际文件格式修改读取方式)
# df = pd.read_csv('你的课程数据文件.csv') 
# 假设基金日收益率列名为 'fund'
# daily_returns = df['fund']

# ---- 以下为计算核心代码 ----
# 假设 daily_returns 已经获取到，是一个 pandas Series

# 参数设置
rf_annual = 0.021       # 年化无风险利率 2.1%
trading_days = 252      # 一年的交易日天数

# 计算日无风险利率
rf_daily = rf_annual / trading_days

# 计算日超额收益的均值
mean_excess_daily = daily_returns.mean() - rf_daily

# 计算日收益率的标准差 (样本标准差)
std_daily = daily_returns.std()

# 计算年化 Sharpe Ratio
sharpe_annual = (mean_excess_daily / std_daily) * np.sqrt(trading_days)

# 按照输出契约存入字典
result = {
    'sharpe_annual': sharpe_annual
}

# 打印结果
print(result)
