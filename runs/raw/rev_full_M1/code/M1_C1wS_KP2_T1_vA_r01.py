import numpy as np

# 输入参数
risk_free_rate = 0.023  # 无风险利率（年化）
market_return = 0.094   # 市场期望收益（年化）
betas = {
    'X': 0.62,
    'Y': 1.18,
    'Z': 1.51
}
actual_return_y = 0.131  # Y 股票的实际年收益

# 1. 计算每只股票的期望收益（CAPM）
def calculate_expected_return(beta, rf, market_ret):
    return rf + beta * (market_ret - rf)

expected_returns = {
    'er_x': calculate_expected_return(betas['X'], risk_free_rate, market_return),
    'er_y': calculate_expected_return(betas['Y'], risk_free_rate, market_return),
    'er_z': calculate_expected_return(betas['Z'], risk_free_rate, market_return)
}

# 2. 计算 Y 股票的 alpha
alpha_y = actual_return_y - expected_returns['er_y']

# 3. 填充 result 字典
result = {
    'er_x': expected_returns['er_x'],
    'er_y': expected_returns['er_y'],
    'er_z': expected_returns['er_z'],
    'alpha_y': alpha_y
}

# 输出结果（供验证，实际使用时可注释掉）
print(result)
