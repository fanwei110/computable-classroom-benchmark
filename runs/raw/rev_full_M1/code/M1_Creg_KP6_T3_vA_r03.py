import numpy as np
import pandas as pd

# 假设数据文件名为 'course_data.csv'，且包含 'fund' 列
# 如果文件名或路径不同，请修改此处
file_path = 'course_data.csv'

# 读取数据
data = pd.read_csv(file_path)

# 提取 fund 列的收益率数据（假设数据为日频收益率）
fund_returns = data['fund'].dropna().values  # 转换为 numpy 数组并去除缺失值

# 无风险利率（年化，2.1%）
risk_free_rate_annual = 0.021

# 计算日频无风险利率（假设一年有252个交易日）
risk_free_rate_daily = risk_free_rate_annual / 252

# 计算超额收益率（fund 收益率 - 无风险利率）
excess_returns = fund_returns - risk_free_rate_daily

# 计算超额收益率的均值和标准差
mean_excess_return = np.mean(excess_returns)
std_excess_return = np.std(excess_returns, ddof=1)  # 样本标准差（ddof=1）

# 计算年化夏普比率
# 年化均值 = 日频均值 * 252
# 年化标准差 = 日频标准差 * sqrt(252)
sharpe_ratio_annual = (mean_excess_return * 252) / (std_excess_return * np.sqrt(252))

# 将结果存入 result 字典
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果（可选，用于验证）
print(result)
