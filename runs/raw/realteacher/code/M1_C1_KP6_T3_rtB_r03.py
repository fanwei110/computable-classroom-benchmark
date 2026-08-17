import numpy as np
import pandas as pd

# 假设 df 是包含基金日收益的DataFrame，fund 列为日收益率
# 示例代码（请根据实际数据调整）

# 计算日超额收益
risk_free_daily = (1 + 0.021) ** (1/252) - 1
excess_return = df['fund'] - risk_free_daily

# 计算超额收益的均值和标准差
mean_excess_return = excess_return.mean()
std_excess_return = excess_return.std()

# 计算年化夏普比率
sharpe_annual = (mean_excess_return * np.sqrt(252)) / std_excess_return

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}

print(result)
