import numpy as np

# 给定参数
risk_free_rate = 0.023  # 无风险利率 2.3%
market_expected_return = 0.094  # 市场期望收益 9.4%
betas = {
    'x': 0.62,
    'y': 1.18,
    'z': 1.51
}
actual_return_y = 0.131  # 股票 Y 当年实际收益 13.1%

# 计算 CAPM 期望收益
def calculate_capm_expected_return(beta, risk_free_rate, market_expected_return):
    return risk_free_rate + beta * (market_expected_return - risk_free_rate)

# 计算各股票的期望收益
expected_return_x = calculate_capm_expected_return(betas['x'], risk_free_rate, market_expected_return)
expected_return_y = calculate_capm_expected_return(betas['y'], risk_free_rate, market_expected_return)
expected_return_z = calculate_capm_expected_return(betas['z'], risk_free_rate, market_expected_return)

# 计算股票 Y 的 alpha
alpha_y = actual_return_y - expected_return_y

# 结果存入字典
result = {
    'er_x': expected_return_x,
    'er_y': expected_return_y,
    'er_z': expected_return_z,
    'alpha_y': alpha_y
}

# 输出结果（可选，题目未要求打印，但为了验证可复现性）
print(result)
