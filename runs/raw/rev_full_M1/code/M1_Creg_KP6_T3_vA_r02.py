import numpy as np
import pandas as pd

# 设定无风险利率（年化）
risk_free_rate_annual = 0.021

# 读取数据文件（假设文件名为 'course_data.csv'，且包含 'fund' 列）
# 注：实际使用时需确保文件路径正确
try:
    data = pd.read_csv('course_data.csv')
    fund_returns = data['fund'].dropna().values  # 提取 fund 列并去除缺失值
except FileNotFoundError:
    raise FileNotFoundError("请确保数据文件 'course_data.csv' 存在且包含 'fund' 列")
except KeyError:
    raise KeyError("数据文件中未找到 'fund' 列")

# 计算日频收益率的均值和标准差
mean_daily_return = np.mean(fund_returns)
std_daily_return = np.std(fund_returns, ddof=1)  # 样本标准差（ddof=1）

# 年化处理
trading_days_per_year = 252
mean_annual_return = mean_daily_return * trading_days_per_year
std_annual_return = std_daily_return * np.sqrt(trading_days_per_year)

# 计算年化夏普比率
sharpe_ratio_annual = (mean_annual_return - risk_free_rate_annual) / std_annual_return

# 存储结果
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果（可选，用于验证）
print("年化夏普比率:", result['sharpe_annual'])
