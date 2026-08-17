import pandas as pd
import numpy as np

# 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 设定参数
risk_free_rate_annual = 0.021  # 2.1%
trading_days = 252

# 计算日无风险利率
risk_free_rate_daily = risk_free_rate_annual / trading_days

# 提取 fund 列的日收益率（假设已是小数形式）
fund_returns = df['fund'].values

# 计算超额日收益
excess_returns_daily = fund_returns - risk_free_rate_daily

# 计算年化夏普比率
# 分子：年化平均超额收益 = 日均超额收益 * 252
# 分母：年化波动率 = 日超额收益标准差 * sqrt(252)
mean_excess_daily = np.mean(excess_returns_daily)
std_excess_daily = np.std(excess_returns_daily, ddof=1)  # 样本标准差

sharpe_annual = (mean_excess_daily * trading_days) / (std_excess_daily * np.sqrt(trading_days))

# 存储结果
result = {
    'sharpe_annual': sharpe_annual
}

# 打印结果以便验证
print(f"年化夏普比率: {sharpe_annual:.6f}")
print(f"结果字典: {result}")
