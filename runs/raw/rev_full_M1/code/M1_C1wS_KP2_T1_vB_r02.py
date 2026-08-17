import numpy as np

# 输入参数
risk_free_rate = 0.023  # 无风险收益率 2.3%
market_return = 0.094   # 市场预期收益率 9.4%
betas = {
    'X': 0.62,
    'Y': 1.18,
    'Z': 1.51
}
actual_return_y = 0.131  # Y 股票实际收益率 13.1%

# 计算 CAPM 预期收益率
def calculate_capm_er(rf, beta, rm):
    return rf + beta * (rm - rf)

# 计算每只股票的预期收益率
er_x = calculate_capm_er(risk_free_rate, betas['X'], market_return)
er_y = calculate_capm_er(risk_free_rate, betas['Y'], market_return)
er_z = calculate_capm_er(risk_free_rate, betas['Z'], market_return)

# 计算 Y 股票的 alpha
alpha_y = actual_return_y - er_y

# 存储结果
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果（可选，用于验证）
print("CAPM 预期收益率:")
print(f"X: {er_x:.4f}")
print(f"Y: {er_y:.4f}")
print(f"Z: {er_z:.4f}")
print(f"\nY 股票的 alpha: {alpha_y:.4f}")
