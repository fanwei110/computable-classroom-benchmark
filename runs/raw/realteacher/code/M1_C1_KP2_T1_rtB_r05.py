# 计算期望收益率
er_x = 2.3 + 0.62 * (9.4 - 2.3)
er_y = 2.3 + 1.18 * (9.4 - 2.3)
er_z = 2.3 + 1.51 * (9.4 - 2.3)

# 计算Y的Alpha
alpha_y = 13.1 - er_y

# 存入字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

result
