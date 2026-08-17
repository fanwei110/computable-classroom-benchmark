import pandas as pd
import numpy as np

# 假设数据已加载，变量名为 fund
# 若 fund 为 DataFrame 且含 'fund' 列，则提取该列；若 fund 本身就是 Series，则直接使用
if isinstance(fund, pd.DataFrame):
    fund_series = fund['fund']
else:
    fund_series = fund

# 判断数据是净值还是收益率：如果最大值显著大于1，则认为是净值数据，需计算日收益率
if fund_series.max() > 1.5:
    daily_returns = fund_series.pct_change().dropna()
else:
    daily_returns = fund_series

# 无风险利率参数
rf_annual = 0.021
rf_daily = rf_annual / 252  # 将年化无风险利率转为日度

# 计算年化夏普比率
mean_daily = daily_returns.mean()
std_daily = daily_returns.std()

sharpe_daily = (mean_daily - rf_daily) / std_daily
sharpe_annual = sharpe_daily * np.sqrt(252)

# 按照输出契约存入字典
result = {'sharpe_annual': sharpe_annual}
