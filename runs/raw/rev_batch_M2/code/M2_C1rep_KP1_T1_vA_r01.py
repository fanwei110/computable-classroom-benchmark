import numpy as np

# 给定数据
vol = np.array([0.187, 0.243, 0.312])
rho = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37,  1.0]
])

# 协方差矩阵
cov = np.diag(vol) @ rho @ np.diag(vol)

# 最小方差组合（允许卖空，全额投资）
inv_cov = np.linalg.inv(cov)
ones = np.ones(3)
w_mvp = inv_cov @ ones
w_mvp = w_mvp / np.sum(w_mvp)

# 组合年化波动率
var_mvp = w_mvp @ cov @ w_mvp
vol_mvp = np.sqrt(var_mvp)

result = {
    'mvp_weights': np.round(w_mvp, 4).tolist(),
    'mvp_vol_annual': round(vol_mvp, 4)
}
result
