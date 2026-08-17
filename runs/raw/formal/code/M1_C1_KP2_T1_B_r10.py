# 计算预期收益
rf = 0.023
rm = 0.094
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

er_x = rf + beta_x * (rm - rf)
er_y = rf + beta_y * (rm - rf)
er_z = rf + beta_z * (rm - rf)

# 计算Y的Alpha
actual_return_y = 0.131
alpha_y = actual_return_y - er_y

# 存入result字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

result
