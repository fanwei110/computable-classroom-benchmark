import numpy as np
import pandas as pd

# 1. 读取数据
data_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(data_path, parse_dates=['date'])

# 提取 fund 列的日收益率
daily_returns = df['fund'].dropna().values  # 确保无缺失值

# 2. 计算日无风险利率
annual_rf_rate = 0.021
daily_rf_rate = annual_rf_rate / 252

# 计算超额收益（日收益 - 日无风险利率）
excess_returns = daily_returns - daily_rf_rate

# 3. 计算样本标准差（ddof=1）
sample_std = np.std(excess_returns, ddof=1)

# 年化夏普比率 = 平均超额收益 / 年化波动率
mean_excess_return = np.mean(excess_returns)
annualized_volatility = sample_std * np.sqrt(252)
sharpe_annual = mean_excess_return / sample_std * np.sqrt(252)  # 等价于 mean_excess_return / (sample_std / np.sqrt(252))

# 4. 存储结果
result = {
    'sharpe_annual': sharpe_annual
}
