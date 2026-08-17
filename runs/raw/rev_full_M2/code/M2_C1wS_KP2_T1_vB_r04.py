# 自包含的 CAPM 计算脚本
# 给定参数（小数形式）
rf = 0.023          # 无风险利率 2.3%
market_return = 0.094  # 市场期望收益 9.4%
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_return_y = 0.131  # Y 股票的实际收益 13.1%

# 1. CAPM 公式：E[Ri] = rf + beta_i * (E[Rm] - rf)
market_premium = market_return - rf
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 2. Y 股票的 alpha = 实际收益 - CAPM 预测收益
alpha_y = actual_return_y - er_y

# 3. 按要求将结果存入字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出供教师投屏查看
print(result)
