import numpy as np

# 课程计算约定
rf = 0.023          # 无风险利率（年化，小数）
market_er = 0.094   # 市场期望收益（年化，小数）
betas = {
    'x': 0.62,
    'y': 1.18,
    'z': 1.51
}

# 1. 计算各股票的 CAPM 期望收益
er_x = rf + betas['x'] * (market_er - rf)
er_y = rf + betas['y'] * (market_er - rf)
er_z = rf + betas['z'] * (market_er - rf)

# 2. 计算股票 Y 的 alpha
actual_er_y = 0.131  # 股票 Y 当年实际收益（小数）
alpha_y = actual_er_y - er_y

# 3. 填充 result 字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印结果以供课堂展示
print(result)
