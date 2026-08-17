import numpy as np

# 假设 fund 是一个 pandas Series，包含基金的收益率数据
# 无风险利率
risk_free_rate = 0.021

# 计算超额收益率
excess_returns = fund - risk_free_rate / 12  # 如果是月度数据，无风险利率也要调整为月度

# 计算超额收益率的均值和标准差
mean_excess_return = excess_returns.mean()
std_excess_return = excess_returns.std()

# 年化夏普比率
# 假设数据是月度数据，年化因子为12（均值）和 sqrt(12)（标准差）
annualized_sharpe = (mean_excess_return * 12) / (std_excess_return * np.sqrt(12))

# 存入结果字典
result = {
    'sharpe_annual': annualized_sharpe
}
