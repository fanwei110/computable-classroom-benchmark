import numpy as np

# ==========================================
# 《证券投资学》课堂实时编程：CAPM与Alpha计算
# ==========================================

# 1. 定义已知参数（统一转换为小数形式以便计算）
rf = 0.023          # 无风险利率 rf = 2.3%
rm = 0.094          # 市场期望收益 E[Rm] = 9.4%
betas = np.array([0.62, 1.18, 1.51])  # X, Y, Z 的 beta 值
actual_return_y = 0.131  # Y 的实际收益率 = 13.1%

# 2. 套用 CAPM 公式：E[Ri] = rf + beta * (E[Rm] - rf)
market_risk_premium = rm - rf
expected_returns = rf + betas * market_risk_premium

# 提取各股票的期望收益
er_x = expected_returns[0]
er_y = expected_returns[1]
er_z = expected_returns[2]

# 3. 计算 Y 的 Alpha：alpha_y = 实际收益 - CAPM 预期收益
alpha_y = actual_return_y - er_y

# 4. 填充结果字典，严格遵循输出契约
result = {
    'er_x': er_x,
    'er_y': er_y,
    'er_z': er_z,
    'alpha_y': alpha_y
}

# ==========================================
# 课堂投屏展示辅助打印（可选，便于学生阅读验证）
# ==========================================
print("=" * 50)
print("CAPM 与证券市场线计算结果")
print("=" * 50)
print(f"市场风险溢价 [E(Rm) - Rf]: {market_risk_premium:.4%}")
print("-" * 50)
print(f"股票 X (Beta={betas[0]}): E[Rx] = {er_x:.4%}")
print(f"股票 Y (Beta={betas[1]}): E[Ry] = {er_y:.4%}")
print(f"股票 Z (Beta={betas[2]}): E[Rz] = {er_z:.4%}")
print("-" * 50)
print(f"股票 Y 实际收益: {actual_return_y:.4%}")
print(f"股票 Y 的 Alpha: {alpha_y:.4%}")
print("=" * 50)

# 验证输出契约
# print(result)
