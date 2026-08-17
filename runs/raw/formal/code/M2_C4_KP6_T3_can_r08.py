import pandas as pd
import numpy as np

# 读取数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列，并剔除缺失值
fund = df['fund'].dropna()

# 判断 fund 列是价格还是收益率：若大部分绝对值大于1，则视为价格，计算日简单收益率
if (fund.abs() > 1).any():
    # 当做价格序列，计算日收益率
    fund_ret = fund.pct_change().dropna()
else:
    # 已经是日收益率序列
    fund_ret = fund.copy()

# 无风险利率年化 2.1%，折算成日无风险利率
rf_annual = 0.021
rf_daily = rf_annual / 252

# 计算超额日收益率
excess_return = fund_ret - rf_daily

# 样本均值与样本标准差（ddof=1）
mean_excess_daily = excess_return.mean()
std_excess_daily = excess_return.std(ddof=1)

# 年化夏普比率
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(252)

# 结果存入字典，键名严格为 'sharpe_annual'
result = {'sharpe_annual': sharpe_annual}

# 输出结果，供投屏展示
print(result)
