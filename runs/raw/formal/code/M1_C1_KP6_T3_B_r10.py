import numpy as np

# 假设 fund 是基金的收益率序列（例如日度收益率），rf 是年化无风险收益率
fund = np.array(fund)  # 替换为实际数据
rf = 0.021  # 年化无风险收益率

# 计算年化收益率和年化标准差
annualized_return = np.mean(fund) * 252  # 假设日度数据，年化乘数为252
annualized_volatility = np.std(fund) * np.sqrt(252)  # 年化波动率

# 计算年化超额收益
excess_return = annualized_return - rf

# 计算年化夏普比率
sharpe_annual = excess_return / annualized_volatility

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
