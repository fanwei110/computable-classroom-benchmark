import numpy as np

# 给定参数
rf = 0.023          # 无风险利率
rm = 0.094          # 市场期望收益
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_y = 0.131    # 股票 Y 的实际年收益

# 1. 计算 CAPM 期望收益
er_x = rf + beta_x * (rm - rf)
er_y = rf + beta_y * (rm - rf)
er_z = rf + beta_z * (rm - rf)

# 2. 计算股票 Y 的 alpha
alpha_y = actual_y - er_y

# 3. 填充结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果（投屏展示）
print(result)
