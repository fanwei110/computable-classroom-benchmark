import numpy as np

# 假设 fund_returns 是基金的全样本收益率（例如日收益率列表）
# 这里以示例数据为例（请替换为实际数据）
fund_returns = np.array([0.001, -0.002, 0.003, 0.0005, -0.001, ...])  # 示例数据

# 年化无风险收益率
rf_annual = 0.021

# 计算年化收益率
annual_return = np.mean(fund_returns) * 252  # 假设日收益率，252个交易日

# 计算年化收益标准差（波动率）
annual_volatility = np.std(fund_returns) * np.sqrt(252)

# 计算年化夏普比率
sharpe_annual = (annual_return - rf_annual) / annual_volatility

# 存入 result 字典
result = {
    'sharpe_annual': sharpe_annual
}

print(result)
