import numpy as np
import pandas as pd

# 1. 读取数据
data_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(data_path)

# 提取 fund 列的日收益率
daily_returns = df['fund'].dropna().values  # 确保无缺失值

# 2. 计算日超额收益
annual_rf_rate = 0.021
daily_rf_rate = annual_rf_rate / 252
excess_returns = daily_returns - daily_rf_rate

# 3. 计算年化夏普比率
mean_excess_return = np.mean(excess_returns)
std_excess_return = np.std(excess_returns, ddof=1)  # 样本标准差
sharpe_daily = mean_excess_return / std_excess_return
sharpe_annual = sharpe_daily * np.sqrt(252)

# 4. 存储结果
result = {
    'sharpe_annual': sharpe_annual
}
