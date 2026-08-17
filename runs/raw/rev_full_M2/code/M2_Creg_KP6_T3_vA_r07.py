import pandas as pd
import numpy as np

# 读取课程数据文件（请根据实际文件名调整）
# 假设文件名为 course_data.csv，且包含 'fund' 列（每日净值）
df = pd.read_csv('course_data.csv')

# 计算日收益率（简单百分比变化，剔除缺失值）
daily_returns = df['fund'].pct_change().dropna()

# 无风险利率设置
rf_annual = 0.021                  # 年化无风险利率 2.1%
rf_daily = rf_annual / 252         # 日无风险利率（简易年化分解）

# 每日超额收益率
excess_daily = daily_returns - rf_daily

# 年化夏普比率 = (日均超额收益 / 日超额收益标准差) * sqrt(252)
sharpe_annual = np.sqrt(252) * (excess_daily.mean() / excess_daily.std())

# 按要求存入字典
result = {'sharpe_annual': sharpe_annual}

# 输出结果
print(result)
