import numpy as np
import pandas as pd

# 假设数据文件名为 'course_data.csv'，且包含 'fund' 列
# 如果文件名或路径不同，请修改此处
file_path = 'course_data.csv'

# 读取数据
data = pd.read_csv(file_path)

# 提取 fund 列的收益率数据（假设数据已是收益率，若为价格序列需先计算收益率）
fund_returns = data['fund'].dropna().values  # 去除缺失值

# 无风险利率（年化）
risk_free_rate_annual = 0.021

# 计算日频收益率的均值和标准差
mean_return_daily = np.mean(fund_returns)
std_return_daily = np.std(fund_returns, ddof=1)  # 样本标准差

# 年化均值和标准差（假设一年有 252 个交易日）
trading_days_per_year = 252
mean_return_annual = mean_return_daily * trading_days_per_year
std_return_annual = std_return_daily * np.sqrt(trading_days_per_year)

# 计算年化夏普比率
sharpe_ratio_annual = (mean_return_annual - risk_free_rate_annual) / std_return_annual

# 将结果存入 result 字典
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果（可选，用于验证）
print(result)
