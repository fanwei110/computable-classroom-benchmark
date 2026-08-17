import numpy as np

# 波动率
vols = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 协方差矩阵
cov = np.outer(vols, vols) * corr

# 最小方差组合权重 (使用优化方法)
# 这里使用解析解：w = (Σ⁻¹ @ 1) / (1ᵀ @ Σ⁻¹ @ 1)
ones = np.ones(3)
cov_inv = np.linalg.inv(cov)
mvp_weights = cov_inv @ ones / (ones.T @ cov_inv @ ones)

# 组合波动率
mvp_vol = np.sqrt(mvp_weights.T @ cov @ mvp_weights)

result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol)
}
