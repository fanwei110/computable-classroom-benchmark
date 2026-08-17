import numpy as np
import pandas as pd

# 假设 fund 是包含每日收益率的 Series
# 无风险利率年化为 2.1%，转换为每日无风险利率
risk_free_rate_daily = (1 + 0.021) ** (1/252) - 1

# 计算超额收益
excess_return = fund - risk_free_rate_daily

# 计算超额收益的均值和标准差
mean_excess_return = excess_return.mean()
std_excess_return = excess_return.std()

# 年化夏普比率
sharpe_annual = (mean_excess_return * 252) / (std_excess_return * np.sqrt(252))

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
