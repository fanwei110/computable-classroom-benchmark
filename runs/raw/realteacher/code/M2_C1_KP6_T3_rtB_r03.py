import pandas as pd
import numpy as np

# 读取数据
file_path = "课程数据文件"  # 请替换为实际文件名
df = pd.read_csv(file_path)

# 计算日收益率（假设fund是价格，如果已经是收益率则直接使用）
# 这里先按价格处理：日收益率 = (当日价格 / 前一日价格) - 1
# 如果fund列已经是收益率，则直接使用，但通常数据是净值价格
# 检查列名：可能是'日期'和'fund'
df = df.sort_values('日期')
fund_prices = df['fund'].values
daily_returns = fund_prices[1:] / fund_prices[:-1] - 1

# 年化无风险利率
rf_annual = 0.021
# 日化无风险利率（假设252个交易日）
rf_daily = (1 + rf_annual)**(1/252) - 1

# 超额日收益率
excess_daily = daily_returns - rf_daily

# 年化夏普比率
mean_excess_daily = np.mean(excess_daily)
std_excess_daily = np.std(excess_daily, ddof=1)  # 样本标准差
sharpe_annual = (mean_excess_daily / std_excess_daily) * np.sqrt(252)

# 存入结果字典
result = {'sharpe_annual': sharpe_annual}
