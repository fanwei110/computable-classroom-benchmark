import numpy as np

# 给定数据
vols = np.array([0.187, 0.243, 0.312])
corr = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13,0.37,  1.0 ]
])

# 计算协方差矩阵
Sigma = np.diag(vols) @ corr @ np.diag(vols)
# 最小方差组合权重（允许卖空，全额投资）
ones = np.ones(3)
inv_Sigma = np.linalg.inv(Sigma)
unnorm_w = inv_Sigma @ ones
w_mvp = unnorm_w / np.sum(unnorm_w)
# 组合年化波动率
var_mvp = w_mvp @ Sigma @ w_mvp
vol_mvp = np.sqrt(var_mvp)

result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': vol_mvp
}
