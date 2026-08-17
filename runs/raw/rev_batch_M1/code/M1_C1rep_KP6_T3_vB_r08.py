import numpy as np

# 假设 fund_returns 是基金的全样本日收益率（示例数据）
fund_returns = np.array([0.001, -0.002, 0.003, ...])  # 请替换为实际数据

# 无风险收益率（年化）
rf = 0.021

# 计算年化收益率
annual_return = np.mean(fund_returns) * 252  # 假设252个交易日

# 计算年化波动率
annual_volatility = np.std(fund_returns) * np.sqrt(252)

# 计算年化夏普比率
sharpe_annual = (annual_return - rf) / annual_volatility

# 存入 result 字典
result = {
    'sharpe_annual': sharpe_annual
}

print(result)
