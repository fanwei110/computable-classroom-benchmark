import numpy as np
from scipy.optimize import minimize

# 1. 构造协方差矩阵
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr_matrix = np.array([
    [1.00, 0.21, -0.13],
    [0.21, 1.00,  0.37],
    [-0.13, 0.37, 1.00]
])

# 协方差矩阵 = 波动率对角阵 @ 相关系数矩阵 @ 波动率对角阵
cov_matrix = np.diag(vols) @ corr_matrix @ np.diag(vols)

# 2. 最小方差组合权重（闭式解）
# 目标函数：w'Σw，约束：sum(w) = 1
n = cov_matrix.shape[0]
ones = np.ones(n)
inv_cov = np.linalg.inv(cov_matrix)
mvp_weights = inv_cov @ ones / (ones @ inv_cov @ ones)

# 3. 组合波动率
mvp_vol_annual = np.sqrt(mvp_weights @ cov_matrix @ mvp_weights)

# 4. 填充结果字典
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol_annual)
}

print(result)
