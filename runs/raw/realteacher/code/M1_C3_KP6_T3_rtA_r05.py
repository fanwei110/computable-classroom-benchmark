import numpy as np
import pandas as pd

# 假设df是包含fund列的DataFrame
# df = pd.read_csv('your_data_file.csv')  # 读取数据文件
daily_returns = df['fund']  # 提取日收益率数据

# 计算日收益率的均值和标准差（样本标准差，ddof=1）
mean_daily_return = daily_returns.mean()
std_daily_return = daily_returns.std(ddof=1)

# 年化处理
annualized_return = mean_daily_return * 252
annualized_volatility = std_daily_return * np.sqrt(252)

# 无风险收益率
risk_free_rate = 0.021

# 计算年化夏普比率
sharpe_annual = (annualized_return - risk_free_rate) / annualized_volatility

# 存入result字典
result = {
    'sharpe_annual': sharpe_annual
}
