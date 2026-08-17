import pandas as pd
import numpy as np

# ==================== 假设说明 ====================
# 1. 频率假设：课堂基金数据通常为日度收益率，此处假设一年包含 252 个交易日。
# 2. 无风险利率换算：年化无风险利率 2.1% 除以 252 得到日度无风险利率。
# 3. 年化方法：采用常见的算术平均年化方式，即 E[R] * 252，σ * sqrt(252)。
# 4. 标准差计算：使用样本标准差（ddof=1，pandas默认），符合统计学与金融惯例。
# ==================================================

# 1. 读取快照 CSV
df = pd.read_csv('snapshot.csv')

# 提取基金收益率序列并清理缺失值
fund_returns = df['fund'].dropna()

# 无风险利率（年化 2.1%）
rf_annual = 0.021

# 假设数据为日度频率，一年252个交易日
periods_per_year = 252

# 计算日度无风险利率
rf_period = rf_annual / periods_per_year

# 2. 计算全样本年化夏普比率
# 每期超额收益
excess_returns = fund_returns - rf_period

# 年化夏普比率 = (平均超额收益 / 收益率标准差) * sqrt(周期数)
# 分母使用 fund_returns.std() 为行业惯例（因为无风险资产方差为0）
sharpe_annual = (excess_returns.mean() / fund_returns.std()) * np.sqrt(periods_per_year)

# 3. 把结果存入 result
result = {'sharpe_annual': sharpe_annual}

# 输出结果以供验证
print(result)
