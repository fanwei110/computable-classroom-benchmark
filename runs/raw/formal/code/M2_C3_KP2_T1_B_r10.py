# 给定参数
rf = 0.023        # 无风险利率
market = 0.094    # 市场收益率
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_y = 0.131  # Y股票的实际收益率

# 市场风险溢价
mrp = market - rf  # 0.071

# CAPM预期收益
er_x = rf + beta_x * mrp
er_y = rf + beta_y * mrp
er_z = rf + beta_z * mrp

# Alpha of Y
alpha_y = actual_y - er_y

# 存储结果
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 查看结果
result
