import numpy as np
import pandas as pd

# 1. 读取数据并计入无风险利率
file_path = 'data/market_snapshot_v1.csv'
data = pd.read_csv(file_path)

# 提取fund列（假设fund列代表基金的日收益率）
fund_returns = data['fund'].dropna()  # 去除缺失值

# 无风险利率（年化2.1%，转换为日利率）
risk_free_rate_annual = 0.021
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1

# 计算超额收益率（减去无风险利率）
excess_returns = fund_returns - risk_free_rate_daily

# 2. 计算年化夏普比率
# 日度夏普比率 = 平均超额收益 / 超额收益的标准差
sharpe_daily = excess_returns.mean() / excess_returns.std()

# 年化夏普比率 = 日度夏普比率 * sqrt(252)
sharpe_annual = sharpe_daily * np.sqrt(252)

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_annual
}

# 输出结果（可选，用于验证）
print(result)
