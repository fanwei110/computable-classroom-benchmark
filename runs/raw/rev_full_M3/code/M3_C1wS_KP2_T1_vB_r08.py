import numpy as np

# ==================== 假设与参数设定 ====================
# 题目给定的参数（百分数转换为小数以便计算）
rf = 0.023          # 无风险利率 rf = 2.3%
rm = 0.094          # 市场期望收益 E[Rm] = 9.4%
beta_x = 0.62       # 股票 X 的 Beta
beta_y = 1.18       # 股票 Y 的 Beta
beta_z = 1.51       # 股票 Z 的 Beta
actual_return_y = 0.131  # 股票 Y 的实际收益率 = 13.1%

# ==================== 步骤 1：套用 CAPM 计算 X, Y, Z 的期望收益 ====================
# CAPM 公式: E[Ri] = rf + beta_i * (E[Rm] - rf)
market_premium = rm - rf  # 市场风险溢价

er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# ==================== 步骤 2：计算 Y 的 Alpha ====================
# Alpha 定义为实际收益偏离证券市场线(SML)的部分: alpha = R_actual - E[Ri]
alpha_y = actual_return_y - er_y

# ==================== 步骤 3：填充 result 字典 ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# ==================== 课堂投屏展示辅助 ====================
# 为了投屏效果更直观，将小数转为百分比格式打印
print("=== CAPM 与证券市场线计算结果 ===")
print(f"市场风险溢价 [E(Rm) - Rf]: {market_premium:.4f} ({market_premium*100:.2f}%)")
print("-"---------------------------------)
print(f"股票 X 期望收益 E[Rx]: {er_x:.4f} ({er_x*100:.2f}%)")
print(f"股票 Y 期望收益 E[Ry]: {er_y:.4f} ({er_y*100:.2f}%)")
print(f"股票 Z 期望收益 E[Rz]: {er_z:.4f} ({er_z*100:.2f}%)")
print("-"---------------------------------)
print(f"股票 Y 实际收益: {actual_return_y:.4f} ({actual_return_y*100:.1f}%)")
print(f"股票 Y 的 Alpha: {alpha_y:.4f} ({alpha_y*100:.2f}%)")
print("="=================================")
