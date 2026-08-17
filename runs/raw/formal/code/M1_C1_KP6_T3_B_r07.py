import numpy as np

# 假设 fund 是基金的日收益率序列（例如 numpy array 或 pandas Series）
fund = ...  # 请替换为实际数据
rf_annual = 0.021  # 年化无风险收益率 2.1%

# 计算日无风险收益率
rf_daily = (1 + rf_annual) ** (1 / 252) - 1

# 计算超额收益率
excess_return = fund - rf_daily

# 计算年化夏普比率
sharpe_annual = np.mean(excess_return) / np.std(excess_return) * np.sqrt(252)

# 存入 result 字典
result = {
    'sharpe_annual': sharpe_annual
}
