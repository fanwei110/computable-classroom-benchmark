import numpy as np

# ================= 马科维茨均值-方差组合理论：相关系数对组合波动率的影响 =================

# 1. 确定资产参数与 60/40 权重
# 资产A波动率(18.4%)低于资产B(29.7%)，在经典投资组合语境下，"60/40组合"通常指
# 60%配置于低波动资产(核心防守)，40%配置于高波动资产(进攻)，故设定 A=60%, B=40%
vol_A = 0.184
vol_B = 0.297
weights = np.array([0.6, 0.4])

# 定义两个相关系数场景
rho_before = 0.3
rho_after = 0.8

# 2. 构造相关系数 0.3 与 0.8 两个协方差矩阵
# 协方差公式：Cov(A, B) = rho * vol_A * vol_B
cov_before = np.array([
    [vol_A**2, rho_before * vol_A * vol_B],
    [rho_before * vol_A * vol_B, vol_B**2]
])

cov_after = np.array([
    [vol_A**2, rho_after * vol_A * vol_B],
    [rho_after * vol_A * vol_B, vol_B**2]
])

# 3. 计算两个组合波动率
# 组合方差公式：sigma_p^2 = w'Σw
# 组合年化波动率公式：sigma_p = sqrt(w'Σw)
var_before = weights.T @ cov_before @ weights
var_after = weights.T @ cov_after @ weights

vol_before_annual = np.sqrt(var_before)
vol_after_annual = np.sqrt(var_after)

# 4. 填充 result
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# ================= 课堂展示打印 =================
if __name__ == "__main__":
    print("="*60)
    print("马科维茨组合理论：相关系数变化对 60/40 组合波动率的影响")
    print("="*60)
    print(f"资产A年化波动率: {vol_A:.1%}")
    print(f"资产B年化波动率: {vol_B:.1%}")
    print(f"组合权重: A = {weights[0]:.0%}, B = {weights[1]:.0%}")
    print("-"*60)
    print(f"当相关系数 = {rho_before} 时，组合年化波动率: {result['vol_before_annual']:.4f} ({result['vol_before_annual']:.2%})")
    print(f"当相关系数 = {rho_after} 时，组合年化波动率: {result['vol_after_annual']:.4f} ({result['vol_after_annual']:.2%})")
    print("-"*60)
    change = result['vol_after_annual'] - result['vol_before_annual']
    print(f"波动率变化量: {change:.4f} ({change:.2%})")
    print("结论：相关系数上升，分散化效应减弱，组合波动率增大。")
