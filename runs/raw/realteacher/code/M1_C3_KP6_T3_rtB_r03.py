import numpy as np

# 示例数据（请替换为实际数据）
fund_returns = [...]  # 基金的日收益率列表（小数形式）

# 无风险利率（年化）
rf_annual = 0.021
rf_daily = rf_annual / 252

# 计算日超额收益
excess_returns = np.array(fund_returns) - rf_daily

# 计算超额收益的均值和标准差（样本估计量）
mu_excess = np.mean(excess_returns)
sigma_excess = np.std(excess_returns, ddof=1)

# 年化夏普比率
sharpe_annual = (mu_excess / sigma_excess) * np.sqrt(252)

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
