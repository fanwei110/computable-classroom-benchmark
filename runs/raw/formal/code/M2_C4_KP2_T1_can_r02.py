import numpy as np

# 参数设定（小数表示）
rf = 0.023                     # 无风险利率 2.3%
er_mkt = 0.094                 # 市场期望收益 9.4%
beta_x, beta_y, beta_z = 0.62, 1.18, 1.51   # 各股票 beta
actual_r_y = 0.131             # 股票 Y 实际收益 13.1%

# CAPM 期望收益计算：E[Ri] = rf + beta_i * (E[Rm] - rf)
mrp = er_mkt - rf              # 市场风险溢价
er_x = rf + beta_x * mrp
er_y = rf + beta_y * mrp
er_z = rf + beta_z * mrp

# 股票 Y 的 alpha
alpha_y = actual_r_y - er_y

# 结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 如果需要实时查看结果（投屏展示）
print(result)
