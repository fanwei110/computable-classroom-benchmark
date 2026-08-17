import numpy as np

# 无风险利率（年化）
risk_free_rate_annual = 0.021

# 将年化无风险利率转换为每日无风险利率
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1

# 计算每日超额收益（基金收益率 - 无风险利率）
excess_returns = fund - risk_free_rate_daily

# 计算超额收益的均值和标准差
mean_excess_return_daily = excess_returns.mean()
std_excess_return_daily = excess_returns.std()

# 年化均值和标准差
mean_excess_return_annual = mean_excess_return_daily * 252
std_excess_return_annual = std_excess_return_daily * np.sqrt(252)

# 计算年化夏普比率
sharpe_annual = mean_excess_return_annual / std_excess_return_annual

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
