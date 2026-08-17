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

# 最小方差组合权重 (允许卖空, 全额投资)
inv_cov = np.linalg.inv(cov)
ones = np.ones(3)
w = inv_cov @ ones / (ones @ inv_cov @ ones)

# 组合年化波动率
vol_annual = np.sqrt(w @ cov @ w)

result = {
    'mvp_weights': w.tolist(),
    'mvp_vol_annual': vol_annual
}

# 打印结果以供检查
print(result)
