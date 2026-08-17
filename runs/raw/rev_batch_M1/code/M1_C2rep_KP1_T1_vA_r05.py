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

# 2. 最小方差组合权重（闭式解）
ones = np.ones(3)
inv_cov = np.linalg.inv(cov_matrix)
mvp_weights_raw = inv_cov @ ones
mvp_weights = mvp_weights_raw / mvp_weights_raw.sum()  # 归一化

# 3. 组合波动率
mvp_vol_annual = np.sqrt(mvp_weights @ cov_matrix @ mvp_weights)

# 4. 填充结果字典
result = {
    'mvp_weights': mvp_weights.round(6).tolist(),
    'mvp_vol_annual': round(float(mvp_vol_annual), 6)
}

print(result)
