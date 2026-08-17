# 给定数据
R_f = 0.023    # 无风险利率
R_m = 0.094    # 市场收益率
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_y = 0.131  # Y的实际收益

# 市场风险溢价
premium = R_m - R_f

# CAPM期望收益
er_x = R_f + beta_x * premium
er_y = R_f + beta_y * premium
er_z = R_f + beta_z * premium

# Y的alpha
alpha_y = actual_y - er_y

# 结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印检查（可选）
print(result)
