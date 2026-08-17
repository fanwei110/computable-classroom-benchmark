import numpy as np

# 输入参数
vols = np.array([0.187, 0.243, 0.312])
rhos = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 计算协方差矩阵
cov_matrix = np.outer(vols, vols) * rhos

# 最小方差组合权重 (允许卖空): w = (Σ^{-1} * 1) / (1^T * Σ^{-1} * 1)
inv_cov = np.linalg.inv(cov_matrix)
ones = np.ones(3)
w_mvp = inv_cov @ ones / (ones @ inv_cov @ ones)

# 组合年化波动率
var_mvp = w_mvp @ cov_matrix @ w_mvp
vol_mvp_annual = np.sqrt(var_mvp)

result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': vol_mvp_annual
}
