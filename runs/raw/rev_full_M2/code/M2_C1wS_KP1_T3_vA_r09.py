import numpy as np

# ========== 给定参数 ==========
sigma_A = 0.184       # 资产 A 年化波动率 (18.4%)
sigma_B = 0.297       # 资产 B 年化波动率 (29.7%)
rho_before = 0.3      # 原来的相关系数
rho_after  = 0.8      # 变化后的相关系数

# 投资组合权重：A 占六成、B 占四成
w = np.array([0.6, 0.4])

# ========== 构建协方差矩阵 ==========
def covariance_matrix(sigma_a, sigma_b, rho):
    """返回 2x2 协方差矩阵"""
    cov_ab = rho * sigma_a * sigma_b
    return np.array([[sigma_a**2, cov_ab],
                     [cov_ab, sigma_b**2]])

Sigma_before = covariance_matrix(sigma_A, sigma_B, rho_before)
Sigma_after  = covariance_matrix(sigma_A, sigma_B, rho_after)

# ========== 计算组合波动率（年化） ==========
var_before = w.T @ Sigma_before @ w
var_after  = w.T @ Sigma_after @ w

vol_before_annual = np.sqrt(var_before)
vol_after_annual  = np.sqrt(var_after)

# ========== 输出结果 ==========
result = {
    'vol_before_annual': round(vol_before_annual, 6),  # 保留 6 位小数以确保清晰
    'vol_after_annual' : round(vol_after_annual, 6)
}

# 如需在课堂上直接观察，可打印
print("组合波动率（年化）")
print(f"  相关系数 0.3: {result['vol_before_annual']:.4%}")
print(f"  相关系数 0.8: {result['vol_after_annual']:.4%}")
