import numpy as np

# 假设 daily_returns 是 fund 列的日收益数据（Series 或 array-like）
daily_returns = ...  # 请替换为实际数据

# 无风险利率参数
risk_free_rate_annual = 0.021
trading_days = 252

# 计算日无风险收益率（近似）
risk_free_rate_daily = risk_free_rate_annual / trading_days

# 计算日超额收益
excess_returns = daily_returns - risk_free_rate_daily

# 计算日超额收益的均值和标准差（样本标准差，ddof=1）
mean_excess = np.mean(excess_returns)
std_excess = np.std(excess_returns, ddof=1)

# 年化夏普比率
sharpe_annual = (mean_excess * np.sqrt(trading_days)) / std_excess

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
