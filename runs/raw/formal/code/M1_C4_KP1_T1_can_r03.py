import numpy as np
from scipy.optimize import minimize

# 给定数据
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr = np.array([
    [1.00, 0.21, -0.13],
    [0.21, 1.00,  0.37],
    [-0.13, 0.37, 1.00]
])

# 1. 构造协方差矩阵
cov_matrix = np.outer(vols, vols) * corr

# 2. 最小方差组合权重（闭式解）
n = len(vols)
ones = np.ones(n)
inv_cov = np.linalg.inv(cov_matrix)
w_mvp = inv_cov @ ones / (ones @ inv_cov @ ones)  # 归一化使和为1

# 3. 组合波动率
mvp_vol = np.sqrt(w_mvp @ cov_matrix @ w_mvp)

# 4. 填充结果字典
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(mvp_vol)
}
