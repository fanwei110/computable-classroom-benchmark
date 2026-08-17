import numpy as np

# 给定年化波动率
sigma = np.array([0.187, 0.243, 0.312])
# 相关系数矩阵
rho = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13,0.37,  1.0 ]
])
# 计算协方差矩阵
Sigma = np.diag(sigma) @ rho @ np.diag(sigma)

# 最小方差组合（允许卖空，权重和为1）
ones = np.ones(3)
Sigma_inv = np.linalg.inv(Sigma)
w_mvp = Sigma_inv @ ones / (ones @ Sigma_inv @ ones)

# 组合年化波动率
mvp_vol = np.sqrt(w_mvp @ Sigma @ w_mvp)

# 结果字典
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': mvp_vol
}

# 输出查看（实际使用时直接返回 result）
print(result)
