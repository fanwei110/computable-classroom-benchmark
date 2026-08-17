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

# 计算 CAPM 期望收益
def calculate_capm_er(beta):
    return risk_free_rate + beta * (market_return - risk_free_rate)

# 计算各股票的期望收益
er_x = calculate_capm_er(betas['x'])
er_y = calculate_capm_er(betas['y'])
er_z = calculate_capm_er(betas['z'])

# 计算股票 Y 的 alpha
alpha_y = actual_return_y - er_y

# 存储结果
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果（可选，用于验证）
print(result)
