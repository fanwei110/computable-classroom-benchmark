import numpy as np

# ==================== 1. 输入参数设定 (小数表示) ====================
rf = 0.023       # 无风险利率 2.3%
rm = 0.094       # 市场期望收益 9.4%

beta_x = 0.62    # 股票 X 的 beta
beta_y = 1.18    # 股票 Y 的 beta
beta_z = 1.51    # 股票 Z 的 beta

real_return_y = 0.131  # 股票 Y 的当年实际收益 13.1%

# ==================== 2. 套用 CAPM 公式计算期望收益 ====================
# E[Ri] = rf + beta * (E[Rm] - rf)
market_risk_premium = rm - rf

er_x = rf + beta_x * market_risk_premium
er_y = rf + beta_y * market_risk_premium
er_z = rf + beta_z * market_risk_premium

# ==================== 3. 计算 Y 的 Alpha ====================
# Alpha = 实际收益 - CAPM 期望收益
alpha_y = real_return_y - er_y

# ==================== 4. 填充 result 字典 ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# ==================== 5. 控制台输出 (供课堂投屏验证) ====================
print("《证券投资学》课堂实时计算演示：CAPM 与 Alpha")
print("-" * 45)
print(f"无风险利率 (rf):        {rf:.3f} ({rf*100:.1f}%)")
print(f"市场期望收益 (E[Rm]):   {rm:.3f} ({rm*100:.1f}%)")
print(f"市场风险溢价 (E[Rm]-rf):{market_risk_premium:.4f} ({market_risk_premium*100:.2f}%)")
print("-" * 45)
print(f"股票 X (Beta={beta_x}): E[Rx] = {er_x:.5f} ({er_x*100:.2f}%)")
print(f"股票 Y (Beta={beta_y}): E[Ry] = {er_y:.5f} ({er_y*100:.2f}%)")
print(f"股票 Z (Beta={beta_z}): E[Rz] = {er_z:.5f} ({er_z*100:.2f}%)")
print("-" * 45)
print(f"股票 Y 实际收益:         {real_return_y:.3f} ({real_return_y*100:.1f}%)")
print(f"股票 Y Alpha:          {alpha_y:.5f} ({alpha_y*100:.2f}%)")
print("-" * 45)
print("\n最终输出字典 result:")
for key, value in result.items():
    print(f"  '{key}': {value}")
