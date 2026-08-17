# 给定数据
rf = 0.023  # 无风险收益率
rm = 0.094  # 市场收益率
betas = {'x': 0.62, 'y': 1.18, 'z': 1.51}  # 各股票的贝塔系数
actual_return_y = 0.131  # Y的实际收益

# 计算预期收益
er_x = rf + betas['x'] * (rm - rf)
er_y = rf + betas['y'] * (rm - rf)
er_z = rf + betas['z'] * (rm - rf)

# 计算Y的Alpha
alpha_y = actual_return_y - er_y

# 存入结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

print(result)
