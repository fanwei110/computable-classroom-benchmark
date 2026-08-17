import numpy as np

# 给定数据（小数形式）
sigma = np.array([0.187, 0.243, 0.312])
rho = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37,  1.0]
])

# 构造协方差矩阵
Sigma = np.outer(sigma, sigma) * rho

# 最小方差组合：允许卖空，全额投资 (sum w = 1)
ones = np.ones(len(sigma))
inv_Sigma = np.linalg.inv(Sigma)
w_mvp = inv_Sigma @ ones / (ones @ inv_Sigma @ ones)

# 组合年化波动率（小数）
vol_mvp = np.sqrt(w_mvp @ Sigma @ w_mvp)

result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': vol_mvp
}
