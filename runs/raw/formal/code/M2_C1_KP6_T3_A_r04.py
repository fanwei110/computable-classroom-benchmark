import pandas as pd
import numpy as np

# 读取数据，假设 'fund' 列是日收益率（小数形式）
df = pd.read_csv('你的数据.csv')  # 替换为实际文件
fund_returns = df['fund']

rf_annual = 0.021
# 假设日频数据
rf_daily = rf_annual / 252
n = 252

excess = fund_returns - rf_daily
sharpe_annual = (excess.mean() / excess.std()) * np.sqrt(n)

result = {'sharpe_annual': sharpe_annual}
