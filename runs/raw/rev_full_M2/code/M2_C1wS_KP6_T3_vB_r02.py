import pandas as pd
import numpy as np

# 读取数据（请确保文件名为“快照.csv”，且与脚本同目录）
df = pd.read_csv('快照.csv')

# 假设 'fund' 列为每期简单收益率（小数形式，例如 0.01 代表 1%）
# 数据频率假设为日度；若实际为其他频率，请对应修改 trading_days 与 rf 的处理方式
trading_days = 252          # 年交易日数
rf_annual = 0.021           # 年化无风险利率 2.1%
rf_period = rf_annual / trading_days   # 日无风险利率

# 移除缺失值，确保计算稳健
fund_returns = df['fund'].dropna()

# 计算超额收益率
excess_returns = fund_returns - rf_period

# 全样本均值与标准差
mean_excess = excess_returns.mean()
std_excess = excess_returns.std(ddof=1)  # 样本标准差（无偏估计）

# 日度夏普比率
sharpe_daily = mean_excess / std_excess

# 年化夏普比率
sharpe_annual = sharpe_daily * np.sqrt(trading_days)

# 输出结果字典
result = {
    'sharpe_annual': sharpe_annual
}

print(result)
