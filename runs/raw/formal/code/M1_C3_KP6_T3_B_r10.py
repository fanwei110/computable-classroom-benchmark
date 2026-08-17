import numpy as np

# 假设 fund 是包含基金日收益率的 pandas Series
# 例如：fund = pd.Series([0.001, -0.002, 0.003, ...])

# 计算日收益率的均值和标准差
mean_daily_return = fund.mean()
daily_volatility = fund.std(ddof=1)  # 样本标准差

# 年化收益率和波动率
annual_return = mean_daily_return * 252
annual_volatility = daily_volatility * np.sqrt(252)

# 年化夏普比率
rf = 0.021  # 无风险利率
sharpe_annual = (annual_return - rf) / annual_volatility

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
