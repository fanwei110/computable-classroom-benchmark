import pandas as pd
import numpy as np

# 1. 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 2. 设定无风险利率 (年化 2.1% 转换为日化)
rf_annual = 0.021
rf_daily = rf_annual / 252

# 3. 计算日超额收益
# 假设 'fund' 列直接给出日收益率（小数形式，例如 0.001 表示 0.1%）
# 若 'fund' 为净值价格，则需先计算日收益率: df['fund_return'] = df['fund'].pct_change()
# 并丢弃第一行 NaN: excess_return = df['fund_return'].dropna() - rf_daily
excess_return = df['fund'] - rf_daily

# 4. 计算样本均值与样本标准差 (ddof=1)
mean_excess = excess_return.mean()
std_excess = excess_return.std(ddof=1)   # 样本标准差

# 5. 年化夏普比率 (sqrt(252) 缩放)
sharpe_annual = np.sqrt(252) * mean_excess / std_excess

# 6. 存入结果字典
result = {'sharpe_annual': sharpe_annual}

# 输出结果供查看
print(result)
