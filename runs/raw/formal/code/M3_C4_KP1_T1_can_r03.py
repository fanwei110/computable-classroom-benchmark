import numpy as np

# ==========================================
# 马科维茨均值-方差组合理论：全局最小方差组合计算
# ==========================================

# 1. 已知数据（小数表示）
sigmas = np.array([0.187, 0.243, 0.312])
corr_matrix = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37, 1.0 ]
])

# 2. 构造协方差矩阵 Σ (Σ_ij = ρ_ij * σ_i * σ_j)
cov_matrix = np.outer(sigmas, sigmas) * corr_matrix

# 3. 求全局最小方差组合（MVP）权重
# 闭式解：w_mvp = Σ^{-1} * 1 / (1' * Σ^{-1} * 1)
# 为保证数值稳定性，使用 np.linalg.solve 求解 Σ * x = 1
ones = np.ones(3)
Sigma_inv_ones = np.linalg.solve(cov_matrix, ones)  # 等价于 cov_matrix的逆 乘以 ones

# 归一化使其和为1
mvp_weights = Sigma_inv_ones / np.sum(Sigma_inv_ones)

# 4. 计算组合波动率（标准差）
# 组合方差 = w'Σw，波动率取平方根
mvp_var = mvp_weights.T @ cov_matrix @ mvp_weights
mvp_vol = np.sqrt(mvp_var)

# 5. 按要求键名填充结果
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol)
}

# 输出结果，方便课堂投屏验证
print("全局最小方差组合权重:", result['mvp_weights'])
print("权重之和:", sum(result['mvp_weights']))
print("全局最小方差组合年化波动率:", result['mvp_vol_annual'])
