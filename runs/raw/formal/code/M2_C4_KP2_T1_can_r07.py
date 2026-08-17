import numpy as np

# 给定参数（小数表示）
rf = 0.023          # 无风险利率 2.3%
rm = 0.094          # 市场期望收益 9.4%
market_premium = rm - rf   # 市场风险溢价

# 各股票的 beta
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# 股票Y的实际年收益
actual_return_y = 0.131   # 13.1%

# 1. 用 CAPM 公式计算期望收益: E[R] = rf + beta * (rm - rf)
er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# 2. 计算股票Y的 alpha = 实际收益 - CAPM期望收益
alpha_y = actual_return_y - er_y

# 3. 将结果存入 result 字典，键名严格按要求
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# 打印结果以供课堂投屏展示
print("CAPM 计算结果（小数表示）")
print(f"无风险利率 rf = {rf:.4f}")
print(f"市场期望收益 rm = {rm:.4f}")
print(f"市场风险溢价 = {market_premium:.4f}")
print("-" * 40)
print(f"股票 X (beta={beta_x}): 期望收益 er_x = {er_x:.6f} ({er_x*100:.4f}%)")
print(f"股票 Y (beta={beta_y}): 期望收益 er_y = {er_y:.6f} ({er_y*100:.4f}%)")
print(f"股票 Z (beta={beta_z}): 期望收益 er_z = {er_z:.6f} ({er_z*100:.4f}%)")
print("-" * 40)
print(f"股票 Y 实际收益 = {actual_return_y:.4f} ({actual_return_y*100:.2f}%)")
print(f"股票 Y 的 alpha = {alpha_y:.6f} ({alpha_y*100:.4f}%)")

# 验证 result 字典内容
print("\nresult 字典内容：")
for key, value in result.items():
    print(f"  {key}: {value}")
