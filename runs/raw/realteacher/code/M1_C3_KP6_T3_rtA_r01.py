import numpy as np

# 假设fund列的日收益率数据存储在变量daily_returns中
# 示例：daily_returns = np.array([...])  # 替换为实际数据

# 计算日收益率的均值和标准差（样本标准差，ddof=1）
mean_daily_return = np.mean(daily_returns)
std_daily_return = np.std(daily_returns, ddof=1)

# 年化收益率和波动率
annualized_return = mean_daily_return * 252
annualized_volatility = std_daily_return * np.sqrt(252)

# 无风险收益率（2.1%）
risk_free_rate = 0.021

# 计算超额收益率
excess_return = annualized_return - risk_free_rate

# 计算年化夏普比率
sharpe_annual = excess_return / annualized_volatility

# 存入result字典
result = {
    'sharpe_annual': sharpe_annual
}
