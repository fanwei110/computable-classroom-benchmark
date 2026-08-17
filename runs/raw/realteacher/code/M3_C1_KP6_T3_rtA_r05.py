import numpy as np
import pandas as pd

# 假设数据已经加载到名为 df 的 DataFrame 中，且包含 'fund' 列
# df = pd.read_csv('your_data_file.csv') 

# 参数设定
rf_annual = 0.021  # 年化无风险利率 2.1%
trading_days = 252 # 一年的交易日天数

# 计算日无风险利率（通常按单利折算到日均）
rf_daily = rf_annual / trading_days

# 计算日收益的均值和标准差（样本标准差 ddof=1）
mean_daily = df['fund'].mean()
std_daily = df['fund'].std()

# 计算年化夏普比率
# 日夏普 = (日均值 - 日无风险) / 日标准差
# 年化夏普 = 日夏普 * sqrt(252)
sharpe_daily = (mean_daily - rf_daily) / std_daily
sharpe_annual = sharpe_daily * np.sqrt(trading_days)

# 按照输出契约存入字典
result = {
    'sharpe_annual': sharpe_annual
}
