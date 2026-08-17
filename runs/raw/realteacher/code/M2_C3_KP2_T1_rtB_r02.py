# 给定参数
rf = 0.023          # 无风险利率
market_return = 0.094  # 市场期望收益
market_premium = market_return - rf  # 市场风险溢价

# 贝塔系数
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# Y的实际收益
actual_y = 0.131

# CAPM 期望收益计算
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# Y的alpha
alpha_y = actual_y - er_y

# 结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

result
