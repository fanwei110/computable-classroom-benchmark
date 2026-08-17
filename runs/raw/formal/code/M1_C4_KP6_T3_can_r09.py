import pandas as pd
import numpy as np

# 读取数据
data_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(data_path)

# 提取fund列的日收益率
daily_returns = df['fund'].dropna().values  # 转为numpy数组并去除缺失值

# 计算日无风险利率（年利率2.1%）
annual_rf_rate = 0.021
daily_rf_rate = annual_rf_rate / 252

# 计算超额收益（日收益率 - 日无风险利率）
excess_returns = daily_returns - daily_rf_rate

# 计算样本标准差（ddof=1）
daily_volatility = np.std(excess_returns, ddof=1)

# 计算年化夏普比率
annualized_sharpe = np.mean(excess_returns) / daily_volatility * np.sqrt(252)

# 存储结果
result = {
    'sharpe_annual': annualized_sharpe
}

# 输出结果（可选，方便调试）
print(result)
