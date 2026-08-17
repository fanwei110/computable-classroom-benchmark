import pandas as pd
import numpy as np

# 1. 读取数据并设定无风险利率
file_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(file_path)
risk_free_rate = 0.021  # 年化无风险利率2.1%

# 提取fund列（假设fund列代表基金的收益率）
fund_returns = df['fund'].dropna()

# 2. 计算年化夏普比率
# 日频数据转年化：乘以252个交易日
annualized_excess_return = (fund_returns.mean() - risk_free_rate / 252) * 252
annualized_volatility = fund_returns.std() * np.sqrt(252)
sharpe_ratio_annual = annualized_excess_return / annualized_volatility

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果（可选，用于验证）
print(result)
