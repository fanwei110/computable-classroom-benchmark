
# 给定参数
R_f = 2.3       # 无风险利率（%）
R_m = 9.4       # 市场期望收益（%）
beta = {
    'X': 0.62,
    'Y': 1.18,
    'Z': 1.51
}
actual_return_Y = 13.1  # Y的实际年收益（%）

# 市场风险溢价
market_premium = R_m - R_f  # 7.1%

# CAPM期望收益计算函数
def capm_er(beta, R_f, market_premium):
    return R_f + beta * market_premium

# 计算期望收益
er_x = capm_er(beta['X'], R_f, market_premium)
er_y = capm_er(beta['Y'], R_f, market_premium)
er_z = capm_er(beta['Z'], R_f, market_premium)

# 计算Alpha
alpha_y = actual_return_Y - er_y

# 存储结果
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印结果以验证
result
