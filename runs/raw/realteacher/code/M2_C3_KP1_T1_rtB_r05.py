import numpy as np

# 给定数据
sigma = np.array([0.187, 0.243, 0.312])
rho = np.array([
    [1.00, 0.21, -0.13],
    [0.21, 1.00, 0.37],
    [-0.13, 0.37, 1.00]
])

# 年化协方差矩阵
cov = np.diag(sigma) @ rho @ np.diag(sigma)

# 最小方差组合权重（允许卖空，全额投资）
inv_cov = np.linalg.inv(cov)
ones = np.ones(3)
w_mvp = inv_cov @ ones / (ones @ inv_cov @ ones)

# 组合年化波动率
vol_mvp = np.sqrt(w_mvp @ cov @ w_mvp)

result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(vol_mvp)
}
