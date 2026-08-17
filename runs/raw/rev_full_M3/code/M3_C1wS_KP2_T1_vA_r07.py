import numpy as np

# ==================== 1. 参数设定 ====================
rf = 0.023          # 无风险利率 2.3%
rm = 0.094          # 市场期望收益 9.4%
beta_x = 0.62       # 股票 X 的 beta
beta_y = 1.18       # 股票 Y 的 beta
beta_z = 1.51       # 股票 Z 的 beta
actual_return_y = 0.131  # 股票 Y 的实际年收益 13.1%

# ==================== 2. 套用 CAPM 公式 ====================
# E[Ri] = rf + beta_i * (E[Rm] - rf)
market_premium = rm - rf

er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# ==================== 3. 计算 Y 的 Alpha ====================
# alpha = 实际收益 - CAPM 期望收益
alpha_y = actual_return_y - er_y

# ==================== 4. 填充 result 字典 ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# ==================== 5. 课堂投屏打印展示 ====================
print("【CAPM 与证券市场线计算结果】")
print(f"市场风险溢价 (E[Rm] - rf): {market_premium:.4f} ({market_premium*100:.2f}%)")
print("-" * 40)
print(f"股票 X 的期望收益 (er_x): {er_x:.4f} ({er_x*100:.2f}%)")
print(f"股票 Y 的期望收益 (er_y): {er_y:.4f} ({er_y*100:.2f}%)")
print(f"股票 Z 的期望收益 (er_z): {er_z:.4f} ({er_z*100:.2f}%)")
print("-" * 40)
print(f"股票 Y 的实际收益: {actual_return_y:.4f} ({actual_return_y*100:.1f}%)")
print(f"股票 Y 的 Alpha (alpha_y): {alpha_y:.4f} ({alpha_y*100:.2f}%)")
