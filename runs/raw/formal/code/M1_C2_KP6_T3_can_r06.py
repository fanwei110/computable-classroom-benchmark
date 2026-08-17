import pandas as pd
import numpy as np

# 1. 读取数据并设定无风险利率
file_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(file_path)

# 提取 fund 列（假设 fund 列代表基金的日收益率）
fund_returns = df['fund'].dropna()  # 去除缺失值

# 无风险利率（年化）
risk_free_rate_annual = 0.021
# 转换为日无风险利率（假设一年252个交易日）
risk_free_rate_daily = risk_free_rate_annual / 252

# 2. 计算超额收益率
excess_returns = fund_returns - risk_free_rate_daily

# 计算年化夏普比率
# 夏普比率 = 平均超额收益率 / 超额收益率的标准差
mean_excess_return_daily = np.mean(excess_returns)
std_excess_return_daily = np.std(excess_returns, ddof=1)  # 样本标准差

# 年化处理
sharpe_ratio_annual = (mean_excess_return_daily / std_excess_return_daily) * np.sqrt(252)

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果（可选，用于验证）
print(result)
