import pandas as pd
import numpy as np

# 1. 读取数据并设定无风险利率
file_path = 'data/market_snapshot_v1.csv'
data = pd.read_csv(file_path)
risk_free_rate = 0.021  # 年化无风险利率2.1%

# 提取fund列（假设fund列代表基金的日收益率）
fund_returns = data['fund'].dropna()

# 2. 计算年化夏普比率
# 日收益率转换为年化收益率
annualized_return = np.mean(fund_returns) * 252
# 日收益率标准差转换为年化波动率
annualized_volatility = np.std(fund_returns) * np.sqrt(252)
# 计算夏普比率（年化）
sharpe_ratio_annual = (annualized_return - risk_free_rate) / annualized_volatility

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果（可选，用于验证）
print(result)
