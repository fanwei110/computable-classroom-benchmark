import numpy as np

# ==================== 1. 参数设定 ====================
rf = 0.023          # 无风险利率 2.3%
rm = 0.094          # 市场期望收益 9.4%
beta_x = 0.62       # 股票 X 的 beta
beta_y = 1.18       # 股票 Y 的 beta
beta_z = 1.51       # 股票 Z 的 beta
r_y_actual = 0.131  # 股票 Y 的实际年收益 13.1%

# ==================== 2. 套用 CAPM 公式 ====================
# E[Ri] = rf + beta * (E[Rm] - rf)
market_premium = rm - rf

er_x = rf + beta_x * market_premium
er_y = rf + beta_y * market_premium
er_z = rf + beta_z * market_premium

# ==================== 3. 计算 Y 的 Alpha ====================
# Alpha = 实际收益 - CAPM 期望收益
alpha_y = r_y_actual - er_y

# ==================== 4. 填充结果字典 ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# ==================== 5. 控制台输出展示(辅助讲课时投屏) ====================
print("=" * 50)
print("《证券投资学》- CAPM 与证券市场线计算结果")
print("=" * 50)
print(f"无风险利率 (rf): {rf:.1%}")
print(f"市场期望收益 (E[Rm]): {rm:.1%}")
print(f"市场风险溢价 (E[Rm]-rf): {market_premium:.1%}")
print("-" * 50)
print(f"股票 X (Beta={beta_x}): E[Rx] = {er_x:.4%}")
print(f"股票 Y (Beta={beta_y}): E[Ry] = {er_y:.4%}")
print(f"股票 Z (Beta={beta_z}): E[Rz] = {er_z:.4%}")
print("-" * 50)
print(f"股票 Y 实际收益: {r_y_actual:.1%}")
print(f"股票 Y Alpha: {alpha_y:.4%}")
print("=" * 50)
print("\n返回的结果字典 result:")
print(result)
