import numpy as np
import pandas as pd

# 读取数据文件（假设文件名为 'course_data.csv'，且包含 'fund' 列）
# 注意：实际使用时需确保文件路径正确
data = pd.read_csv('course_data.csv')  # 请根据实际文件名调整

# 提取 fund 列的数据
fund_returns = data['fund'].dropna()  # 去除缺失值

# 无风险利率（年化，2.1%）
risk_free_rate_annual = 0.021

# 计算日频超额收益率（假设数据为日频）
excess_returns = fund_returns - (risk_free_rate_annual / 252)  # 252 个交易日/年

# 计算年化夏普比率
sharpe_ratio_annual = np.sqrt(252) * excess_returns.mean() / excess_returns.std()

# 将结果存入 result 字典
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果（可选，用于验证）
print(result)
