import numpy as np
import pandas as pd

# 给定参数
rf = 0.023          # 无风险利率
rm = 0.094          # 市场期望收益
market_premium = rm - rf  # 市场风险溢价

# 各股票的 beta 值
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# 1. 根据 CAPM 计算期望年收益
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 2. 股票 Y 的实际收益与 alpha
actual_y = 0.131
alpha_y = actual_y - er_y

# 3. 填充结果字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 可选：打印结果以便课堂投屏查看
print("CAPM 计算结果：")
print(f"无风险利率 (rf): {rf:.4f} ({rf*100:.2f}%)")
print(f"市场期望收益 (rm): {rm:.4f} ({rm*100:.2f}%)")
print(f"市场风险溢价 (rm-rf): {market_premium:.4f} ({market_premium*100:.2f}%)")
print("-" * 40)
print(f"股票 X   beta: {beta_x:.2f}   CAPM 期望收益: {er_x:.4f} ({er_x*100:.2f}%)")
print(f"股票 Y   beta: {beta_y:.2f}   CAPM 期望收益: {er_y:.4f} ({er_y*100:.2f}%)")
print(f"股票 Z   beta: {beta_z:.2f}   CAPM 期望收益: {er_z:.4f} ({er_z*100:.2f}%)")
print("-" * 40)
print(f"股票 Y 实际收益: {actual_y:.4f} ({actual_y*100:.2f}%)")
print(f"股票 Y alpha:    {alpha_y:.4f} ({alpha_y*100:.2f}%)")
print("-" * 40)
print("结果字典 result =", result)
