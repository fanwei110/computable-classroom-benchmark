import pandas as pd
import numpy as np

# 1. 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 fund 列的日收益率
fund_returns = df['fund']

# 2. 计算日无风险利率与日超额收益
# 课程约定：年利率折算日利率用简单除法（年/252），无风险利率为 2.1% 即 0.021
rf_annual = 0.021
rf_daily = rf_annual / 252

# 日收益减去日无风险利率
excess_returns = fund_returns - rf_daily

# 3. 计算全样本夏普比率并年化
# 计算超额收益的样本均值
mean_excess = np.mean(excess_returns)

# 计算超额收益的样本标准差（ddof=1）
std_excess = np.std(excess_returns, ddof=1)

# 计算日夏普比率
sharpe_daily = mean_excess / std_excess

# 按照课程约定年化：乘以 sqrt(252)
sharpe_annual = sharpe_daily * np.sqrt(252)

# 4. 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}

# 打印结果供课堂投屏查看
print(f"年化夏普比率: {result['sharpe_annual']:.6f}")
