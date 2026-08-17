import pandas as pd
import numpy as np

# 读取快照数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 检查 fund 列是否存在
if 'fund' not in df.columns:
    raise KeyError("数据中缺少 'fund' 列，请检查 CSV 文件")

# 删除缺失值，确保收益率序列完整
fund_returns = df['fund'].dropna()

# 无风险利率（年化小数形式）
rf_annual = 0.021
rf_daily = rf_annual / 252  # 课程约定：年利率折算日为简单除法

# 计算日超额收益
excess_daily = fund_returns - rf_daily

# 全样本日超额收益的均值与标准差（样本标准差，ddof=1）
mean_excess_daily = excess_daily.mean()
std_excess_daily = excess_daily.std(ddof=1)

# 日夏普比率
sharpe_daily = mean_excess_daily / std_excess_daily

# 年化夏普比率（按 sqrt(252) 缩放）
sharpe_annual = sharpe_daily * np.sqrt(252)

# 按要求存入结果字典
result = {'sharpe_annual': sharpe_annual}

print(result)
