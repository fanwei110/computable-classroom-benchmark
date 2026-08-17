import numpy as np
import pandas as pd

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
    stock: calculate_expected_return(beta, risk_free_rate, market_return)
    for stock, beta in betas.items()
}

# 2. 计算 Y 股票的 alpha
alpha_y = actual_return_y - expected_returns['Y']

# 3. 填充 result 字典
result = {
    'er_x': expected_returns['X'],
    'er_y': expected_returns['Y'],
    'er_z': expected_returns['Z'],
    'alpha_y': alpha_y
}

# 输出结果（可选，便于调试）
print("Result dictionary:")
print(result)
