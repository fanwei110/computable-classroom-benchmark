import numpy as np

# 给定参数
risk_free_rate = 0.023  # 无风险利率 2.3%
market_return = 0.094   # 市场期望收益 9.4%
betas = {
    'x': 0.62,
    'y': 1.18,
    'z': 1.51
}
actual_return_y = 0.131  # 股票 Y 实际收益 13.1%

# 计算市场风险溢价
market_risk_premium = market_return - risk_free_rate

# 计算各股票的 CAPM 期望收益
expected_returns = {
    stock: risk_free_rate + beta * market_risk_premium
    for stock, beta in betas.items()
}

# 计算股票 Y 的 alpha
alpha_y = actual_return_y - expected_returns['y']

# 存储结果
result = {
    'er_x': expected_returns['x'],
    'er_y': expected_returns['y'],
    'er_z': expected_returns['z'],
    'alpha_y': alpha_y
}

# 输出结果（可选，用于验证）
print(result)
