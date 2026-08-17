import numpy as np
import pandas as pd

# 假设课程数据已经加载为 DataFrame df，且 'fund' 列为基金的日收益率序列
# daily_returns = df['fund'] 

# 如果 'fund' 列是净值序列，则需要先计算日收益率：
# daily_returns = df['fund'].pct_change().dropna()

# ----------------- 计算过程 -----------------

# 1. 计算日平均收益率与日标准差（样本估计量 ddof=1）
mean_daily = daily_returns.mean()
std_daily = daily_returns.std(ddof=1)

# 2. 年化收益率与年化波动率
# 年化收益率 = 日均收益率 * 252
annual_return = mean_daily * 252

# 年化波动率 = 日标准差 * sqrt(252)
annual_volatility = std_daily * np.sqrt(252)

# 3. 无风险利率
rf = 0.021

# 4. 计算年化夏普比率
# Sharpe = (年化收益率 - 无风险利率) / 年化波动率
sharpe_annual = (annual_return - rf) / annual_volatility

# ----------------- 输出契约 -----------------
result = {
    'sharpe_annual': sharpe_annual
}
