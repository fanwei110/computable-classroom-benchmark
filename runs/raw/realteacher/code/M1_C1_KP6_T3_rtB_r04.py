import numpy as np
import pandas as pd

# 假设df是包含fund列的DataFrame
# 示例代码（请替换为实际数据加载方式）
# df = pd.read_csv('your_course_data_file.csv')

# 计算日超额收益
daily_risk_free_rate = (1 + 0.021) ** (1/252) - 1
excess_returns = df['fund'] - daily_risk_free_rate

# 计算年化夏普比率
mean_excess_return = excess_returns.mean()
std_excess_return = excess_returns.std()
sharpe_annual = (mean_excess_return / std_excess_return) * np.sqrt(252)

# 存入result字典
result = {
    'sharpe_annual': sharpe_annual
}
