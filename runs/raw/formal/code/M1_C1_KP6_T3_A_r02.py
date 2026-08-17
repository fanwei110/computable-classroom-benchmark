import numpy as np

# 假设 fund 是包含每日收益率的 pandas Series
daily_returns = fund

# 无风险利率 (年化 2.1%，转换为每日)
risk_free_rate_annual = 0.021
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1  # 假设252个交易日

# 计算每日超额收益
excess_returns = daily_returns - risk_free_rate_daily

# 计算年化夏普比率
sharpe_annual = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
