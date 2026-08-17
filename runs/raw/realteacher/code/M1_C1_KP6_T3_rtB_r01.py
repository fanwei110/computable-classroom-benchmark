import numpy as np
import pandas as pd

# 假设df是你的数据框，fund列是基金的日收益率
# 示例代码（请根据实际数据调整）

# 读取数据（示例，请替换为实际数据读取方式）
# df = pd.read_csv('your_course_data.csv')

# 计算日超额收益
risk_free_daily = (1 + 0.021) ** (1/252) - 1
df['excess_return'] = df['fund'] - risk_free_daily

# 计算年化夏普比率
mean_excess_return = df['excess_return'].mean()
std_excess_return = df['excess_return'].std()
sharpe_annual = (mean_excess_return * 252) / (std_excess_return * np.sqrt(252))

# 存入结果字典
result = {
    'sharpe_annual': sharpe_annual
}
