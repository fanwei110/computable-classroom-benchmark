import numpy as np

# 年化波动率
vols = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr_matrix = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 协方差矩阵
cov_matrix = np.outer(vols, vols) * corr_matrix

# 计算 MVP 权重
ones = np.ones(3)
cov_inv = np.linalg.inv(cov_matrix)
mvp_weights = cov_inv @ ones / (ones.T @ cov_inv @ ones)

# 计算组合波动率
mvp_vol = np.sqrt(mvp_weights.T @ cov_matrix @ mvp_weights)

# 存入结果
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': mvp_vol.item()
}
