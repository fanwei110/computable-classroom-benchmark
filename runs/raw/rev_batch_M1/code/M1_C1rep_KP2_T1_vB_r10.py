# 计算预期收益
rf = 2.3 / 100
rm = 9.4 / 100
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

er_x = rf + beta_x * (rm - rf)
er_y = rf + beta_y * (rm - rf)
er_z = rf + beta_z * (rm - rf)

# 计算Y的Alpha
actual_return_y = 13.1 / 100
alpha_y = actual_return_y - er_y

# 将结果存入字典
result = {
    'er_x': er_x * 100,  # 转换为百分比形式
    'er_y': er_y * 100,
    'er_z': er_z * 100,
    'alpha_y': alpha_y * 100
}

result
