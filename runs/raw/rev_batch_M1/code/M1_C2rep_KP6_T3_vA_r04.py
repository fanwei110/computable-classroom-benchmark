import numpy as np
import pandas as pd

# 1. 读取数据并设定无风险利率
file_path = 'data/market_snapshot_v1.csv'
data = pd.read_csv(file_path)
risk_free_rate = 0.021  # 年化无风险利率2.1%

# 提取fund列的收益率数据
fund_returns = data['fund'].dropna()

# 2. 计算年化夏普比率
# 日频收益率转年化收益率和波动率
annual_factor = 252  # 假设每年252个交易日
excess_returns = fund_returns - (risk_free_rate / annual_factor)  # 日频超额收益

# 计算年化超额收益和年化波动率
annualized_excess_return = excess_returns.mean() * annual_factor
annualized_volatility = excess_returns.std() * np.sqrt(annual_factor)

# 计算年化夏普比率
sharpe_ratio_annual = annualized_excess_return / annualized_volatility

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果以供验证（非必须，但方便调试）
print(result)
