import pandas as pd
import numpy as np

# 假设 fund 列是基金的日收益率序列，数据已从课程数据中读取
# 例：df = pd.read_csv('course_data.csv')
# fund = df['fund']

# 若无实际数据，此处生成示例数据以便演示计算过程
# 实际计算时请替换为真实数据
np.random.seed(42)
dates = pd.date_range('2018-01-01', '2022-12-31', freq='B')
fund = pd.Series(np.random.normal(0.0005, 0.015, len(dates)), index=dates)  # 模拟日收益率

# 无风险利率
risk_free = 0.021

# 年化收益率（假设每年252个交易日）
annual_return = fund.mean() * 252

# 年化波动率
annual_vol = fund.std() * np.sqrt(252)

# 年化夏普比率
sharpe_annual = (annual_return - risk_free) / annual_vol

result = {'sharpe_annual': sharpe_annual}
print(result)
