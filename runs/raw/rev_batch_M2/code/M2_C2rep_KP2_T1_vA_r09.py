import numpy as np

# 给定参数
rf = 0.023          # 无风险利率
rm = 0.094          # 市场期望收益
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51
actual_y = 0.131    # 股票Y当年实际收益

# 市场风险溢价
market_premium = rm - rf  # 0.071

# CAPM期望收益计算
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 股票Y的alpha
alpha_y = actual_y - er_y

# 按要求填充结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果（便于课堂投屏查看）
if __name__ == "__main__":
    for key, value in result.items():
        print(f"{key}: {value:.6f} ({value*100:.4f}%)")
