import numpy as np

# 输入参数（小数表示）
rf = 0.023          # 无风险利率 2.3%
rm = 0.094          # 市场期望收益 9.4%
market_premium = rm - rf  # 市场风险溢价

# 各股票的 beta
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# 1. 计算 CAPM 期望收益
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 2. 股票 Y 的实际收益与 alpha
actual_y = 0.131  # 13.1%
alpha_y = actual_y - er_y

# 3. 存入结果字典（所有值均为小数）
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 输出结果（供投屏展示）
print("CAPM 计算结果（小数）:")
print(f"市场风险溢价: {market_premium:.6f} ({market_premium*100:.2f}%)")
print(f"股票X期望收益: {er_x:.6f} ({er_x*100:.2f}%)")
print(f"股票Y期望收益: {er_y:.6f} ({er_y*100:.2f}%)")
print(f"股票Z期望收益: {er_z:.6f} ({er_z*100:.2f}%)")
print(f"股票Y实际收益: {actual_y:.4f} ({actual_y*100:.2f}%)")
print(f"股票Y的alpha:  {alpha_y:.6f} ({alpha_y*100:.2f}%)")
print("\n结果字典:")
print(result)
