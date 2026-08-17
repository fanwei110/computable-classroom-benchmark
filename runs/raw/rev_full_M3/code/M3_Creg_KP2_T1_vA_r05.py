import numpy as np

# 给定的输入参数
rf = 0.023        # 无风险利率 2.3%
rm = 0.094        # 市场期望收益 9.4%
beta_x = 0.62     # 股票 X 的 beta
beta_y = 1.18     # 股票 Y 的 beta
beta_z = 1.51     # 股票 Z 的 beta
ry_actual = 0.131 # 股票 Y 实际收益 13.1%

# 计算 CAPM 期望收益: E(Ri) = rf + beta_i * (rm - rf)
market_premium = rm - rf
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 计算股票 Y 的 Alpha: alpha_y = 实际收益 - 期望收益
alpha_y = ry_actual - er_y

# 将结果存入符合要求的字典中
result = {
    'er_x': np.float64(er_x),
    'er_y': np.float64(er_y),
    'er_z': np.float64(er_z),
    'alpha_y': np.float64(alpha_y)
}

# 打印结果以供验证
print(result)
