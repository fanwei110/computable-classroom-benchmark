import pandas as pd
import numpy as np

# 假设数据文件为 'data.csv'，包含 'fund' 列
# df = pd.read_csv('data.csv')
# daily_returns = df['fund'] / 100  # 如果原数据是百分数，需转换；若已是小数则直接使用

# 示例：生成随机数据测试
# np.random.seed(42)
# daily_returns = np.random.normal(0.001, 0.02, 1000)

# 无风险利率
rf_annual = 0.021
rf_daily = (1 + rf_annual) ** (1/252) - 1

# 超额收益
excess_returns = daily_returns - rf_daily

# 年化计算
annual_excess_return = excess_returns.mean() * 252
annual_volatility = excess_returns.std(ddof=1) * np.sqrt(252)

# 夏普比率
sharpe_annual = annual_excess_return / annual_volatility

result = {'sharpe_annual': sharpe_annual}
print(result)
