import numpy as np

# ==================== 输入参数 ====================
# 三只资产的年化波动率（小数形式）
vol_annual = np.array([0.187, 0.243, 0.312])

# 相关系数
corr_12 = 0.21
corr_13 = -0.13
corr_23 = 0.37

# ==================== 构建相关系数矩阵 ====================
corr_matrix = np.array([
    [1.0,  corr_12,  corr_13],
    [corr_12, 1.0,  corr_23],
    [corr_13, corr_23, 1.0 ]
])

# ==================== 构建协方差矩阵 ====================
# 协方差矩阵 Sigma = diag(sigma) @ Corr @ diag(sigma)
cov_matrix = np.outer(vol_annual, vol_annual) * corr_matrix

# ==================== 计算全局最小方差组合 (MVP) ====================
ones = np.ones(3)

# 计算协方差矩阵的逆
inv_cov_matrix = np.linalg.inv(cov_matrix)

# 计算 1^T * Sigma^{-1} * 1
inv_cov_ones = inv_cov_matrix @ ones
ones_inv_cov_ones = ones @ inv_cov_ones

# MVP权重公式: w_mvp = Sigma^{-1} * 1 / (1^T * Sigma^{-1} * 1)
mvp_weights = inv_cov_ones / ones_inv_cov_ones

# MVP方差公式: sigma_mvp^2 = 1 / (1^T * Sigma^{-1} * 1)
mvp_var = 1.0 / ones_inv_cov_ones

# MVP年化波动率
mvp_vol_annual = np.sqrt(mvp_var)

# ==================== 输出结果 ====================
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': mvp_vol_annual
}

print(result)
