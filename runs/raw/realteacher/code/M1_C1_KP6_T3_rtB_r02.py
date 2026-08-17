import numpy as np
import pandas as pd

# 假设df是包含基金日收益率的DataFrame，fund列为基金的日收益率
# 示例代码（请根据实际数据替换）
# df = pd.read_csv('your_course_data_file.csv')
# daily_returns = df['fund']

# 无风险利率的日等价值
risk_free_rate_daily = (1 + 0.021) ** (1/252) - 1

# 计算超额收益率
excess_returns = daily_returns - risk_free_rate_daily

# 计算超额收益率的均值和标准差
mean_excess_return = excess_returns.mean()
std_excess_return = excess_returns.std()

# 计算年化夏普比率
sharpe_annual = (mean_excess_return / std_excess_return) * np.sqrt(252)

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}

print(result)
