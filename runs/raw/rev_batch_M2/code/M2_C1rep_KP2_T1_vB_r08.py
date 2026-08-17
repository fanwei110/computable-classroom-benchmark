# 给定参数
rf = 2.3
market = 9.4
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_y = 13.1

# 市场风险溢价
risk_premium = market - rf

# CAPM 预期收益
er_x = rf + beta_x * risk_premium
er_y = rf + beta_y * risk_premium
er_z = rf + beta_z * risk_premium

# Alpha
alpha_y = actual_y - er_y

result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

result
