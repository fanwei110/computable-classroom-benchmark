import numpy as np  # 可用，但不强制使用

# 给定参数（百分比形式）
rf = 2.3          # 无风险利率 (%)
rm = 9.4          # 市场期望收益 (%)
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_y = 13.1   # 股票 Y 当年实际收益 (%)

# 计算 CAPM 期望收益
er_x = rf + beta_x * (rm - rf)
er_y = rf + beta_y * (rm - rf)
er_z = rf + beta_z * (rm - rf)

# 计算股票 Y 的 alpha
alpha_y = actual_y - er_y

# 按要求存入字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

if __name__ == "__main__":
    print(result)
