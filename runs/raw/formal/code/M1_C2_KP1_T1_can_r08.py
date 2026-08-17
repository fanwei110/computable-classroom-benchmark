import numpy as np
from scipy.optimize import minimize

# 1. 构造协方差矩阵
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr = np.array([
    [1.00, 0.21, -0.13],
    [0.21, 1.00,  0.37],
    [-0.13, 0.37, 1.00]
])

# 协方差矩阵 Σ = diag(vol) @ corr @ diag(vol)
cov_matrix = np.diag(vols) @ corr @ np.diag(vols)

# 2. 最小方差组合权重（满仓约束）
n_assets = len(vols)
ones = np.ones(n_assets)

# 闭式解：w = (Σ⁻¹ @ ones) / (ones' @ Σ⁻¹ @ ones)
inv_cov = np.linalg.inv(cov_matrix)
mvp_weights = inv_cov @ ones
mvp_weights /= mvp_weights.sum()  # 归一化

# 3. 组合波动率
mvp_vol_annual = np.sqrt(mvp_weights @ cov_matrix @ mvp_weights)

# 4. 填充结果字典
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol_annual)
}

print(result)
