import numpy as np
import pandas as pd

# 假设df是包含fund列的DataFrame，fund列为日收益率
# 示例代码（请替换为实际数据加载方式）
# df = pd.read_csv('your_course_data.csv')

# 计算日超额收益
risk_free_daily = (1 + 0.021) ** (1/252) - 1
excess_return = df['fund'] - risk_free_daily

# 计算均值和标准差
mean_excess_return = excess_return.mean()
std_excess_return = excess_return.std()

# 年化处理
annualized_mean = mean_excess_return * 252
annualized_std = std_excess_return * np.sqrt(252)

# 计算年化夏普比率
sharpe_annual = annualized_mean / annualized_std

# 存入result字典
result = {
    'sharpe_annual': sharpe_annual
}
