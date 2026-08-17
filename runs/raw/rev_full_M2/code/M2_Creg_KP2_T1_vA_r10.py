import numpy as np

# 输入数据
Rf = 0.023          # 无风险利率
ERm = 0.094         # 市场期望收益
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_return_y = 0.131  # 股票Y当年实际收益

# 市场风险溢价
market_premium = ERm - Rf

# 计算CAPM期望收益
er_x = Rf + beta_x * market_premium
er_y = Rf + beta_y * market_premium
er_z = Rf + beta_z * market_premium

# 计算股票Y的alpha
alpha_y = actual_return_y - er_y

# 按照输出契约，将结果存入字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果（可复现）
print(result)
