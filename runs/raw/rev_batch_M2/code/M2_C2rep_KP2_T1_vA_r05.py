import numpy as np

# 已知参数
rf = 0.023          # 无风险利率 2.3%
rm = 0.094          # 市场期望收益 9.4%
market_premium = rm - rf  # 市场风险溢价

# 各股票 beta
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# 1. 计算 CAPM 期望收益
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 2. 股票 Y 实际收益与 alpha
actual_y = 0.131     # 13.1%
alpha_y = actual_y - er_y

# 3. 填充结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 可选：打印结果以便课堂投屏观察
if __name__ == "__main__":
    for key, value in result.items():
        print(f"{key}: {value:.6f} ({value*100:.4f}%)")
