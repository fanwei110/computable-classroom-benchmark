import numpy as np
import pandas as pd

# 假设 fund 是包含每日收益率的 Series
# 示例：fund = pd.Series([0.001, -0.002, 0.003, ...])  # 每日收益率

# 无风险利率 (年化 2.1%)
risk_free_rate_annual = 0.021
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1  # 转换为每日无风险利率

# 计算超额收益
excess_returns = fund - risk_free_rate_daily

# 计算年化夏普比率
mean_excess_return_annual = excess_returns.mean() * 252  # 年化均值
std_excess_return_annual = excess_returns.std() * np.sqrt(252)  # 年化标准差
sharpe_annual = mean_excess_return_annual / std_excess_return_annual

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
