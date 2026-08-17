import numpy as np

# 输入参数
rf = 0.023  # 无风险利率（年化）
market_return = 0.094  # 市场期望收益（年化）
betas = {
    'X': 0.62,
    'Y': 1.18,
    'Z': 1.51
}
actual_return_y = 0.131  # Y 股票的实际年收益

# 1. 计算每只股票的期望收益（CAPM）
er_x = rf + betas['X'] * (market_return - rf)
er_y = rf + betas['Y'] * (market_return - rf)
er_z = rf + betas['Z'] * (market_return - rf)

# 2. 计算 Y 股票的 alpha
alpha_y = actual_return_y - er_y

# 3. 填充 result 字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果（可选，用于验证）
print(result)
