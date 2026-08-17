import numpy as np

# 假设已知基金的年化收益率和年化波动率（示例值，请替换为实际数据）
fund_return_annual = 0.08  # 8% 年化收益率（示例）
volatility_annual = 0.10   # 10% 年化波动率（示例）
rf = 0.021                # 无风险收益率 2.1%

# 计算年化夏普比率
sharpe_annual = (fund_return_annual - rf) / volatility_annual

# 存入 result 字典
result = {
    'sharpe_annual': sharpe_annual
}

print(result)
