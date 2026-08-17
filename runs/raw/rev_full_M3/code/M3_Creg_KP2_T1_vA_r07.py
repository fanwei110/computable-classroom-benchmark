import numpy as np

# 已知参数 (转换为小数形式)
rf = 0.023          # 无风险利率 2.3%
erm = 0.094         # 市场期望收益 9.4%
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_ry = 0.131   # 股票 Y 实际收益 13.1%

# 计算市场风险溢价
market_risk_premium = erm - rf

# 使用 CAPM 公式计算各股票的期望收益: E(Ri) = Rf + Beta_i * (E(Rm) - Rf)
er_x = rf + beta_x * market_risk_premium
er_y = rf + beta_y * market_risk_premium
er_z = rf + beta_z * market_risk_premium

# 计算股票 Y 的 Alpha: Alpha = 实际收益 - 期望收益
alpha_y = actual_ry - er_y

# 按照输出契约存入字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印结果以供验证
print(result)
