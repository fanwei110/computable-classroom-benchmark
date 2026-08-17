import numpy as np

# 示例数据（假设 daily_returns 是 fund 列的日收益率序列）
# daily_returns = pd.Series([...])  # 实际数据替换这里

# 无风险收益率（年化 2.1%，转换为日收益率）
risk_free_rate_annual = 0.021
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1

# 计算日超额收益
excess_returns = daily_returns - risk_free_rate_daily

# 计算年化夏普比率
sharpe_annual = np.sqrt(252) * excess_returns.mean() / excess_returns.std()

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
