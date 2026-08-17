import pandas as pd
import numpy as np

# 读取数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取基金日收益率序列（去除缺失值）
fund_ret = df['fund'].dropna()

# 年无风险利率 2.1% 转化为日无风险利率
rf_annual = 0.021
rf_daily = rf_annual / 252

# 计算日超额收益
excess_ret = fund_ret - rf_daily

# 日超额收益的均值和样本标准差（ddof=1 即样本标准差）
mean_excess_daily = excess_ret.mean()
std_excess_daily = excess_ret.std(ddof=1)

# 年化夏普比率：日夏普乘以 sqrt(252)
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(252)

# 输出结果字典
result = {
    'sharpe_annual': sharpe_annual
}

print(result)
