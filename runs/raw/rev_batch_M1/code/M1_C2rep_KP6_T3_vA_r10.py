import pandas as pd
import numpy as np

# 1. 读取数据并设定无风险利率
file_path = 'data/market_snapshot_v1.csv'
risk_free_rate = 0.021  # 年化无风险利率2.1%

# 读取CSV文件，使用fund列
data = pd.read_csv(file_path)
fund_returns = data['fund'].dropna()  # 确保没有缺失值

# 2. 计算年化夏普比率
# 计算日收益率的均值和标准差
daily_mean_return = fund_returns.mean()
daily_std_return = fund_returns.std()

# 年化处理：假设一年有252个交易日
annualized_mean_return = daily_mean_return * 252
annualized_std_return = daily_std_return * np.sqrt(252)

# 计算夏普比率（年化）
sharpe_ratio_annual = (annualized_mean_return - risk_free_rate) / annualized_std_return

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果（可选，用于验证）
print(result)
