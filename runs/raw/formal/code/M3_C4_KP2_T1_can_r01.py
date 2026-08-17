# 《证券投资学》课堂实时编程：CAPM与证券市场线

# 1. 设定已知参数（均以小数表示）
rf = 0.023          # 无风险利率 2.3%
er_m = 0.094        # 市场期望收益 9.4%

beta_x = 0.62       # 股票 X 的 beta
beta_y = 1.18       # 股票 Y 的 beta
beta_z = 1.51       # 股票 Z 的 beta

actual_return_y = 0.131  # 股票 Y 的实际年收益 13.1%

# 2. 套用 CAPM 公式：E[Ri] = rf + beta * (E[Rm] - rf)
market_risk_premium = er_m - rf

er_x = rf + beta_x * market_risk_premium
er_y = rf + beta_y * market_risk_premium
er_z = rf + beta_z * market_risk_premium

# 3. 计算股票 Y 的 alpha：alpha = 实际收益 - CAPM期望收益
alpha_y = actual_return_y - er_y

# 4. 填充 result 字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 课堂投屏输出验证
print(result)
