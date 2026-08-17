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

# 计算每只股票的 CAPM 预期收益
def calculate_capm_er(beta, rf, market_return):
    return rf + beta * (market_return - rf)

# 计算 Y 的 alpha
er_y_capm = calculate_capm_er(betas['Y'], risk_free_rate, market_return)
alpha_y = actual_return_y - er_y_capm

# 存储结果
result = {
    'er_x': calculate_capm_er(betas['X'], risk_free_rate, market_return),
    'er_y': er_y_capm,
    'er_z': calculate_capm_er(betas['Z'], risk_free_rate, market_return),
    'alpha_y': alpha_y
}

# 输出结果（可选，用于验证）
print("CAPM 预期收益和 alpha 计算结果:")
print(f"X 股票预期收益: {result['er_x']:.4f}")
print(f"Y 股票预期收益: {result['er_y']:.4f}")
print(f"Z 股票预期收益: {result['er_z']:.4f}")
print(f"Y 股票 alpha: {result['alpha_y']:.4f}")
