import numpy as np
import pandas as pd

# 1. 读取数据并设定无风险利率
file_path = 'data/market_snapshot_v1.csv'
data = pd.read_csv(file_path)
risk_free_rate = 0.021  # 年化无风险利率2.1%

# 提取fund列的收益率数据
fund_returns = data['fund'].dropna()

# 2. 计算年化夏普比率
# 日度收益率转换为年化收益率和年化波动率
daily_mean_return = fund_returns.mean()
daily_std_return = fund_returns.std()
annual_factor = 252  # 假设每年252个交易日

annualized_return = daily_mean_return * annual_factor
annualized_volatility = daily_std_return * np.sqrt(annual_factor)

# 计算夏普比率（年化）
sharpe_ratio_annual = (annualized_return - risk_free_rate) / annualized_volatility

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果以供验证（可选）
print("年化夏普比率:", result['sharpe_annual'])
