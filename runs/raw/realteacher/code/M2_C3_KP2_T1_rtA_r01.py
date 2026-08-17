# 给定参数
Rf = 0.023
Rm = 0.094
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_return_y = 0.131

# 市场风险溢价
market_premium = Rm - Rf

# CAPM期望收益
er_x = Rf + beta_x * market_premium
er_y = Rf + beta_y * market_premium
er_z = Rf + beta_z * market_premium

# Y的alpha
alpha_y = actual_return_y - er_y

# 按要求存入字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果
print(result)
