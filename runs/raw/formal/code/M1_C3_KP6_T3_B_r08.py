import numpy as np

# 假设fund是基金的净值数据（示例数据）
# fund = np.array([1.00, 1.01, 1.02, 0.99, 1.03, ...])  # 实际数据需替换
# 计算日收益率（simple return）
daily_returns = np.diff(fund) / fund[:-1]

# 年化收益率
annual_return = (1 + np.mean(daily_returns)) ** 252 - 1

# 年化波动率（样本标准差，ddof=1）
annual_volatility = np.std(daily_returns, ddof=1) * np.sqrt(252)

# 无风险利率
rf = 0.021

# 夏普比率
sharpe_annual = (annual_return - rf) / annual_volatility

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
