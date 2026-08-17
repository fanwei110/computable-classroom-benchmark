import pandas as pd
import numpy as np

# 读取数据
data_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(data_path)

# 提取 fund 列的日收益率
daily_returns = df['fund'].dropna().values  # 确保无缺失值

# 无风险利率参数
annual_risk_free_rate = 0.021
daily_risk_free_rate = annual_risk_free_rate / 252

# 计算超额收益（日收益率 - 日无风险利率）
excess_returns = daily_returns - daily_risk_free_rate

# 计算样本均值和样本标准差（ddof=1）
mean_excess_return = np.mean(excess_returns)
std_excess_return = np.std(excess_returns, ddof=1)

# 年化夏普比率
sharpe_annual = mean_excess_return / std_excess_return * np.sqrt(252)

# 存储结果
result = {
    'sharpe_annual': sharpe_annual
}
