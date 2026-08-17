import numpy as np

# ==================== 输入参数 ====================
rf = 0.023          # 无风险利率 2.3%
rm = 0.094          # 市场期望收益 9.4%
beta_x = 0.62       # 股票 X 的 beta
beta_y = 1.18       # 股票 Y 的 beta
beta_z = 1.51       # 股票 Z 的 beta
actual_return_y = 0.131  # 股票 Y 当年实际收益 13.1%

# ==================== 计算步骤 ====================
# 1. 套用 CAPM 公式: E[Ri] = rf + beta * (E[Rm] - rf)
market_risk_premium = rm - rf

er_x = rf + beta_x * market_risk_premium
er_y = rf + beta_y * market_risk_premium
er_z = rf + beta_z * market_risk_premium

# 2. 计算 Y 的 alpha: alpha = 实际收益 - CAPM 期望收益
alpha_y = actual_return_y - er_y

# 3. 填充 result 字典
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# ==================== 课堂投屏展示 ====================
print("="*50)
print("《证券投资学》课堂演示：CAPM 与证券市场线")
print("="*50)
print(f"【输入参数】")
print(f"无风险利率 (rf): {rf*100:.1f}%")
print(f"市场期望收益 (E[Rm]): {rm*100:.1f}%")
print(f"市场风险溢价 (E[Rm]-rf): {market_risk_premium*100:.1f}%")
print("-" * 50)
print(f"【CAPM 期望收益计算】")
print(f"股票 X (Beta={beta_x:.2f}) -> E[Rx] = {er_x*100:.2f}%")
print(f"股票 Y (Beta={beta_y:.2f}) -> E[Ry] = {er_y*100:.2f}%")
print(f"股票 Z (Beta={beta_z:.2f}) -> E[Rz] = {er_z*100:.2f}%")
print("-" * 50)
print(f"【Alpha 计算】")
print(f"股票 Y 实际收益: {actual_return_y*100:.1f}%")
print(f"股票 Y Alpha (实际 - 期望): {alpha_y*100:.2f}%")
print("="*50)

# 验证字典内容
print("\n输出契约字典 result:")
for k, v in result.items():
    print(f"  '{k}': {v:.6f}")
