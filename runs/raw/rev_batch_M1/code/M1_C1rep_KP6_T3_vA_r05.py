import numpy as np

# 假设 fund 是包含每日收益率的 pandas Series
daily_returns = fund

# 无风险利率 (年化 2.1%，转换为每日无风险利率)
risk_free_rate_annual = 0.021
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1  # 假设一年 252 个交易日

# 计算超额收益
excess_returns = daily_returns - risk_free_rate_daily

# 计算超额收益的均值和标准差
mean_excess_return = excess_returns.mean()
std_excess_return = excess_returns.std()

# 年化夏普比率
sharpe_annual = (mean_excess_return / std_excess_return) * np.sqrt(252)

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
