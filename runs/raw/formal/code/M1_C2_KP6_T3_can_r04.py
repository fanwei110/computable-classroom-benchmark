import numpy as np
import pandas as pd

# 1. 读取数据并设定无风险利率
file_path = 'data/market_snapshot_v1.csv'
risk_free_rate = 0.021  # 年化无风险利率2.1%

# 读取CSV文件，提取fund列
data = pd.read_csv(file_path)
fund_returns = data['fund'].dropna()  # 确保没有缺失值

# 2. 计算年化夏普比率
# 日收益率
daily_returns = fund_returns

# 计算超额收益（减去无风险利率的日等价利率）
daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1  # 假设252个交易日
excess_returns = daily_returns - daily_risk_free_rate

# 计算年化超额收益和年化波动率
annualized_excess_return = np.mean(excess_returns) * 252
annualized_volatility = np.std(excess_returns) * np.sqrt(252)

# 计算年化夏普比率
sharpe_annual = annualized_excess_return / annualized_volatility

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_annual
}

# 输出结果以供验证（可选）
print(result)
