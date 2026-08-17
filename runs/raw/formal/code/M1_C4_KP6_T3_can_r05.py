import pandas as pd
import numpy as np

# 读取数据
data_path = 'data/market_snapshot_v1.csv'
market_data = pd.read_csv(data_path)

# 提取fund列的日收益率
daily_returns = market_data['fund']

# 计算日无风险利率（年利率2.1%）
annual_risk_free_rate = 0.021
daily_risk_free_rate = annual_risk_free_rate / 252

# 计算超额收益（日收益减去日无风险利率）
excess_returns = daily_returns - daily_risk_free_rate

# 计算样本标准差（ddof=1）
daily_volatility = np.std(excess_returns, ddof=1)

# 年化夏普比率 = 平均超额收益 / 年化波动率
# 年化波动率 = 日波动率 * sqrt(252)
annualized_volatility = daily_volatility * np.sqrt(252)
mean_excess_return = np.mean(excess_returns)
sharpe_annual = mean_excess_return / daily_volatility * np.sqrt(252)

# 存储结果
result = {
    'sharpe_annual': sharpe_annual
}
