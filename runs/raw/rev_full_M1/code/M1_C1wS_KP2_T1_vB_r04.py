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

# 计算 CAPM 预期收益
def calculate_capm_er(beta, rf, market_er):
    return rf + beta * (market_er - rf)

# 计算每只股票的预期收益
expected_returns = {
    stock: calculate_capm_er(beta, risk_free_rate, market_return)
    for stock, beta in betas.items()
}

# 计算 Y 股票的 alpha
alpha_y = actual_return_y - expected_returns['Y']

# 构建结果字典
result = {
    'er_x': expected_returns['X'],
    'er_y': expected_returns['Y'],
    'er_z': expected_returns['Z'],
    'alpha_y': alpha_y
}

# 输出结果（可选，方便调试）
print(result)
