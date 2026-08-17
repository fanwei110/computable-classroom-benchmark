import numpy as np
import pandas as pd

# 1. 读取数据并设定无风险利率
file_path = 'data/market_snapshot_v1.csv'
risk_free_rate = 0.021  # 年化无风险利率2.1%

# 读取CSV文件，使用fund列
data = pd.read_csv(file_path)
fund_returns = data['fund'].dropna()  # 确保没有缺失值

# 2. 计算年化夏普比率
# 计算日度超额收益
excess_returns = fund_returns - (risk_free_rate / 252)  # 假设252个交易日

# 计算年化均值和标准差
annualized_mean = excess_returns.mean() * 252
annualized_std = excess_returns.std() * np.sqrt(252)

# 计算夏普比率
sharpe_annual = annualized_mean / annualized_std

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_annual
}

# 输出结果以供验证（可选）
print(result)
