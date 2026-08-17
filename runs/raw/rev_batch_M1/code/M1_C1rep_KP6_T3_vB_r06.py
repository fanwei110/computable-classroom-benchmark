import numpy as np

# 假设 fund_returns 是基金的日收益率列表（例如：[0.001, -0.002, ...]）
fund_returns = [...]  # 请替换为实际数据
rf_annual = 0.021  # 年化无风险收益率 2.1%

# 计算年化收益率和波动率
annual_return = np.mean(fund_returns) * 252  # 日收益率年化（假设252交易日）
annual_volatility = np.std(fund_returns) * np.sqrt(252)  # 日收益率年化波动率

# 计算年化夏普比率
sharpe_annual = (annual_return - rf_annual) / annual_volatility

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
