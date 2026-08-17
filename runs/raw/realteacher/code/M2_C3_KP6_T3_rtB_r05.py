import pandas as pd
import numpy as np

# 读取数据，请将文件路径替换成实际文件
df = pd.read_csv('course_data.csv')   # 或其他格式如 .xlsx: pd.read_excel
fund_returns = df['fund']             # 日收益率，小数形式

# 参数设定
rf_annual = 0.021                     # 年化无风险利率 2.1%
trading_days = 252                    # 每年交易日

# 年化平均收益率
mean_daily = fund_returns.mean()
mean_annual = mean_daily * trading_days

# 年化波动率（样本标准差，ddof=1）
std_daily = fund_returns.std(ddof=1)
std_annual = std_daily * np.sqrt(trading_days)

# 年化 Sharpe ratio
sharpe_annual = (mean_annual - rf_annual) / std_annual

# 结果字典
result = {'sharpe_annual': sharpe_annual}
print(result)
