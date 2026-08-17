import pandas as pd
import numpy as np

# 1. 读取数据并设定无风险利率
file_path = 'data/market_snapshot_v1.csv'
data = pd.read_csv(file_path)

# 提取fund列（假设fund列代表基金的日收益率）
daily_returns = data['fund'].dropna()  # 去除缺失值

# 无风险利率（年化2.1%，转换为日利率）
risk_free_rate_annual = 0.021
risk_free_rate_daily = (1 + risk_free_rate_annual) ** (1/252) - 1

# 2. 计算超额收益率
excess_returns = daily_returns - risk_free_rate_daily

# 计算年化夏普比率
# 夏普比率 = 年化超额收益均值 / 年化超额收益标准差
mean_excess_return_daily = excess_returns.mean()
std_excess_return_daily = excess_returns.std()

# 年化处理
trading_days_per_year = 252
annualized_mean_excess = mean_excess_return_daily * trading_days_per_year
annualized_std_excess = std_excess_return_daily * np.sqrt(trading_days_per_year)

sharpe_ratio_annual = annualized_mean_excess / annualized_std_excess

# 3. 存储结果
result = {
    'sharpe_annual': sharpe_ratio_annual
}

# 输出结果（可选，用于验证）
print(result)
