# 给定数据
rf = 0.023
market_return = 0.094
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_return_y = 0.131

# 市场风险溢价
mrp = market_return - rf

# 计算期望收益 (CAPM)
er_x = rf + beta_x * mrp
er_y = rf + beta_y * mrp
er_z = rf + beta_z * mrp

# 计算 alpha_y
alpha_y = actual_return_y - er_y

# 存储结果
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果以便查看
print(result)
