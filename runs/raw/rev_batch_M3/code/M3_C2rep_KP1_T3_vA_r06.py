import numpy as np

# ==================== 1. 确定权重与参数 ====================
# 假设 60/40 权重分别对应资产 A 和资产 B
# 即资产 A 权重为 60%，资产 B 权重为 40%
w = np.array([0.6, 0.4])

# 资产年化波动率
vol_A = 0.184
vol_B = 0.297

# 相关系数设定
rho_before = 0.3
rho_after = 0.8

# ==================== 2. 构造协方差矩阵 ====================
def build_cov_matrix(rho, vol_a, vol_b):
    """根据相关系数和波动率构造协方差矩阵"""
    var_a = vol_a ** 2
    var_b = vol_b ** 2
    cov_ab = rho * vol_a * vol_b
    return np.array([[var_a, cov_ab],
                     [cov_ab, var_b]])

cov_before = build_cov_matrix(rho_before, vol_A, vol_B)
cov_after  = build_cov_matrix(rho_after, vol_A, vol_B)

# ==================== 3. 计算组合波动率 ====================
# 组合方差公式：w'Σw，波动率为方差的开方
var_before = w.T @ cov_before @ w
var_after  = w.T @ cov_after @ w

vol_before_annual = np.sqrt(var_before)
vol_after_annual  = np.sqrt(var_after)

# ==================== 4. 填充 result ====================
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# 课堂投屏展示打印
print(f"相关系数为 {rho_before} 时，60/40 组合的年化波动率: {vol_before_annual:.4%}")
print(f"相关系数为 {rho_after} 时，60/40 组合的年化波动率: {vol_after_annual:.4%}")
print(f"波动率变化量: {(vol_after_annual - vol_before_annual):.4%}")
print("\n字典结果 result:", result)
