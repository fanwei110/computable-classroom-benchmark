import numpy as np
import pandas as pd

# 设定随机种子以确保可复现性（虽然本例不涉及随机性，但保持良好习惯）
np.random.seed(42)

# 假设数据文件名为 'course_data.csv'，且包含 'fund' 列
# 如果文件名或路径不同，请修改此处
file_path = 'course_data.csv'

# 读取数据
try:
    data = pd.read_csv(file_path)
    fund_returns = data['fund'].dropna().values  # 提取 fund 列并去除缺失值
except FileNotFoundError:
    raise FileNotFoundError("请确保数据文件 'course_data.csv' 存在且路径正确。")
except KeyError:
    raise KeyError("数据文件中未找到 'fund' 列。")

# 无风险利率（年化，2.1%）
risk_free_rate_annual = 0.021

# 计算日频超额收益率（假设 fund 列为日频收益率）
excess_returns = fund_returns - (risk_free_rate_annual / 252)  # 252 个交易日/年

# 计算夏普比率（年化）
sharpe_ratio_annual = np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns, ddof=1)

# 存储结果
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果（可选，用于验证）
print(result)
