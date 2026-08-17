import numpy as np

# ==================== 已知参数 ====================
rf = 0.023      # 无风险利率 (2.3%)
erm = 0.094     # 市场期望收益 (9.4%)
betas = np.array([0.62, 1.18, 1.51])  # 股票 X, Y, Z 的 beta
actual_return_y = 0.131  # 股票 Y 的实际收益 (13.1%)

# ==================== 步骤 1：计算 CAPM 期望收益 ====================
# E[Ri] = rf + beta * (E[Rm] - rf)
market_risk_premium = erm - rf

er_x = rf + betas[0] * market_risk_premium
er_y = rf + betas[1] * market_risk_premium
er_z = rf + betas[2] * market_risk_premium

# ==================== 步骤 2：计算股票 Y 的 Alpha ====================
# Alpha = 实际收益 - CAPM 期望收益
alpha_y = actual_return_y - er_y

# ==================== 步骤 3：填充 result 字典 ====================
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# ==================== 控制台输出展示(供投屏参考) ====================
print("=== CAPM 与证券市场线计算结果 ===")
print(f"市场风险溢价 [E(Rm) - Rf]: {market_risk_premium:.4%}\n")

print(f"股票 X (Beta={betas[0]}): E[Rx] = {result['er_x']:.4%}")
print(f"股票 Y (Beta={betas[1]}): E[Ry] = {result['er_y']:.4%}")
print(f"股票 Z (Beta={betas[2]}): E[Rz] = {result['er_z']:.4%}\n")

print(f"股票 Y 实际收益: {actual_return_y:.4%}")
print(f"股票 Y 的 Alpha: {result['alpha_y']:.4%}")
