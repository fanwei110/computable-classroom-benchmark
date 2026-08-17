# 给定参数
rf = 2.3  # 无风险利率（%）
rm = 9.4  # 市场期望收益（%）
market_premium = rm - rf  # 市场风险溢价

# 各股票的beta
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# CAPM期望收益计算
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# Y的实际年收益
actual_y = 13.1  # %
alpha_y = actual_y - er_y

# 按要求组装结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

result
