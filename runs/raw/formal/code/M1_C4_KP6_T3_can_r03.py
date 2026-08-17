import numpy as np
import pandas as pd

# 1. 读取数据
file_path = 'data/market_snapshot_v1.csv'
data = pd.read_csv(file_path)

# 提取 fund 列的日收益率
daily_returns = data['fund'].dropna().values  # 转为 numpy 数组并去除缺失值

# 2. 计算日无风险利率
annual_rf_rate = 0.021
daily_rf_rate = annual_rf_rate / 252

# 计算超额收益（日收益 - 日无风险利率）
excess_returns = daily_returns - daily_rf_rate

# 3. 计算样本标准差（ddof=1）
sample_std = np.std(excess_returns, ddof=1)

# 年化标准差
annualized_volatility = sample_std * np.sqrt(252)

# 计算年化超额收益均值
annualized_excess_return = np.mean(excess_returns) * 252

# 计算年化夏普比率
sharpe_annual = annualized_excess_return / annualized_volatility

# 4. 存储结果
result = {
    'sharpe_annual': sharpe_annual
}
