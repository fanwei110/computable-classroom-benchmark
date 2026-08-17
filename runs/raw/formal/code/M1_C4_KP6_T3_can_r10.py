import numpy as np
import pandas as pd

# 1. 读取数据
data_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(data_path, parse_dates=['date'])

# 提取 fund 列的日收益率
daily_returns = df['fund'].dropna().values  # 确保无缺失值

# 2. 计算日超额收益
annual_rf_rate = 0.021
daily_rf_rate = annual_rf_rate / 252
excess_returns = daily_returns - daily_rf_rate

# 3. 计算样本标准差（ddof=1）
sample_std = np.std(excess_returns, ddof=1)

# 4. 年化夏普比率
mean_excess_return = np.mean(excess_returns)
sharpe_annual = (mean_excess_return / sample_std) * np.sqrt(252)

# 5. 存储结果
result = {
    'sharpe_annual': sharpe_annual
}
