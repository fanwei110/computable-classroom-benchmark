import numpy as np

# 假设 fund_daily_returns 是基金的日收益率序列（全样本）
# 示例数据（请替换为实际数据）
fund_daily_returns = np.array([...])  # 替换为实际日收益率数据

# 计算日均收益率和日波动率
mean_daily_return = np.mean(fund_daily_returns)
std_daily_return = np.std(fund_daily_returns, ddof=1)

# 年化收益率和波动率
annual_return = mean_daily_return * 252
annual_volatility = std_daily_return * np.sqrt(252)

# 年化夏普比率
rf = 0.021  # 无风险利率
sharpe_annual = (annual_return - rf) / annual_volatility

# 存入 result 字典
result = {
    'sharpe_annual': sharpe_annual
}
