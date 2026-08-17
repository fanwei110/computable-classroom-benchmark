import numpy as np

# 资产A和B的年化波动率
sigma_A = 0.184  # 18.4%
sigma_B = 0.297  # 29.7%

# 60/40 组合权重，按顺序对应资产A和资产B
w = np.array([0.6, 0.4])

# 两个情形下的相关系数
rho_before = 0.3
rho_after  = 0.8

# 构造协方差矩阵的函数
def cov_matrix(sigma_A, sigma_B, rho):
    cov_ab = rho * sigma_A * sigma_B
    return np.array([[sigma_A**2, cov_ab],
                     [cov_ab, sigma_B**2]])

Sigma_before = cov_matrix(sigma_A, sigma_B, rho_before)
Sigma_after  = cov_matrix(sigma_A, sigma_B, rho_after)

# 组合方差和年化波动率
var_before = w @ Sigma_before @ w
var_after  = w @ Sigma_after  @ w

vol_before_annual = np.sqrt(var_before)
vol_after_annual  = np.sqrt(var_after)

# 按要求输出到字典 result
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

print(result)
