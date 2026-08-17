import numpy as np

# ==================== 1. 参数设定 ====================
# 所有利率、收益率均以小数表示
rf = 0.023          # 无风险利率 2.3%
rm = 0.094          # 市场期望收益 9.4%

beta_x = 0.62       # 股票 X 的 beta
beta_y = 1.18       # 股票 Y 的 beta
beta_z = 1.51       # 股票 Z 的 beta

actual_return_y = 0.131  # 股票 Y 的实际年收益 13.1%

# ==================== 2. CAPM 计算 ====================
# 市场风险溢价
market_risk_premium = rm - rf

# 套用 CAPM 公式: E[Ri] = rf + beta * (E[Rm] - rf)
er_x = rf + beta_x * market_risk_premium
er_y = rf + beta_y * market_risk_premium
er_z = rf + beta_z * market_risk_premium

# ==================== 3. Alpha 计算 ====================
# Alpha 定义为实际收益减去 CAPM 预测的期望收益
alpha_y = actual_return_y - er_y

# ==================== 4. 填充结果字典 ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# ==================== 5. 控制台输出展示(便于投屏讲解) ====================
print("="*40)
print("《证券投资学》- CAPM 与证券市场线计算")
print("="*40)
print(f"无风险利率 (rf)      : {rf:.3%}")
print(f"市场期望收益 (E[Rm]) : {rm:.3%}")
print(f"市场风险溢价         : {market_risk_premium:.3%}")
print("-" * 40)
print(f"股票 X (Beta={beta_x:.2f})")
print(f"  CAPM 期望收益 (er_x) : {er_x:.5f} ({er_x:.3%})")
print(f"股票 Y (Beta={beta_y:.2f})")
print(f"  CAPM 期望收益 (er_y) : {er_y:.5f} ({er_y:.3%})")
print(f"  实际收益             : {actual_return_y:.5f} ({actual_return_y:.3%})")
print(f"  Alpha (alpha_y)      : {alpha_y:.5f} ({alpha_y:.3%})")
print(f"股票 Z (Beta={beta_z:.2f})")
print(f"  CAPM 期望收益 (er_z) : {er_z:.5f} ({er_z:.3%})")
print("="*40)
print("\n最终 result 字典内容：")
print(result)
