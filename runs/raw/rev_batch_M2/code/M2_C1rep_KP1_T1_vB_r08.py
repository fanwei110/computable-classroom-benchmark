import numpy as np

# 给定的参数
vol = np.array([0.187, 0.243, 0.312])
corr = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 计算协方差矩阵
cov = np.diag(vol) @ corr @ np.diag(vol)

# 计算最小方差组合权重（允许做空，权重之和为1）
one = np.ones(3)
cov_inv = np.linalg.inv(cov)
w_mvp = cov_inv @ one / (one @ cov_inv @ one)

# 计算组合年化波动率
vol_mvp = np.sqrt(w_mvp @ cov @ w_mvp)

# 将结果存入字典
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(vol_mvp)
}

result
