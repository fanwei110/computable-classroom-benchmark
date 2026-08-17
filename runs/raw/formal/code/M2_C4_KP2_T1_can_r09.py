import numpy as np

# ============================================================
# CAPM 计算脚本
# 课程约定：所有利率、收益率用小数表示
# ============================================================

# 给定参数
rf = 0.023        # 无风险利率 (2.3%)
er_m = 0.094      # 市场期望收益 (9.4%)

# 股票 beta
beta_x = 0.62
beta_y = 1.18
beta_z = 1.51

# 股票 Y 实际收益
actual_ret_y = 0.131  # 13.1%

# ------------------------------------------------------------
# 步骤 1：CAPM 期望收益计算
# E[Ri] = rf + beta_i * (E[Rm] - rf)
# ------------------------------------------------------------
er_x = rf + beta_x * (er_m - rf)
er_y = rf + beta_y * (er_m - rf)
er_z = rf + beta_z * (er_m - rf)

# ------------------------------------------------------------
# 步骤 2：计算股票 Y 的 alpha
# alpha = 实际收益 - CAPM 预测收益
# ------------------------------------------------------------
alpha_y = actual_ret_y - er_y

# ------------------------------------------------------------
# 步骤 3：填充结果字典
# ------------------------------------------------------------
result = {
    'er_x': round(er_x, 6),      # 股票 X 的 CAPM 期望收益
    'er_y': round(er_y, 6),      # 股票 Y 的 CAPM 期望收益
    'er_z': round(er_z, 6),      # 股票 Z 的 CAPM 期望收益
    'alpha_y': round(alpha_y, 6) # 股票 Y 的 alpha
}

# 输出结果（投屏展示）
print("=" * 50)
print("CAPM 期望收益与 Alpha 计算结果")
print("=" * 50)
print(f"无风险利率 (rf):         {rf:.4f} ({rf*100:.2f}%)")
print(f"市场期望收益 (E[Rm]):    {er_m:.4f} ({er_m*100:.2f}%)")
print(f"市场风险溢价 (E[Rm]-rf): {er_m - rf:.4f} ({(er_m - rf)*100:.2f}%)")
print("-" * 50)
print(f"股票 X  beta: {beta_x:.2f}  |  CAPM 期望收益: {er_x:.6f} ({er_x*100:.4f}%)")
print(f"股票 Y  beta: {beta_y:.2f}  |  CAPM 期望收益: {er_y:.6f} ({er_y*100:.4f}%)")
print(f"股票 Z  beta: {beta_z:.2f}  |  CAPM 期望收益: {er_z:.6f} ({er_z*100:.4f}%)")
print("-" * 50)
print(f"股票 Y 实际收益: {actual_ret_y:.4f} ({actual_ret_y*100:.2f}%)")
print(f"股票 Y Alpha:    {alpha_y:.6f} ({alpha_y*100:.4f}%)")
print("=" * 50)
print("\n最终结果字典：")
print(result)
