import numpy as np

# 输入数据
vol = np.array([0.187, 0.243, 0.312])
rho = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 构建协方差矩阵
# Cov(i,j) = rho(i,j) * vol_i * vol_j
cov_matrix = np.outer(vol, vol) * rho

# 计算最小方差组合权重
# w_mvp = (Sigma^-1 * 1) / (1^T * Sigma^-1 * 1)
ones = np.ones(3)
cov_inv = np.linalg.inv(cov_matrix)
w_mvp = cov_inv.dot(ones) / ones.dot(cov_inv).dot(ones)

# 计算最小方差组合的年化波动率
# sigma_mvp = sqrt(w^T * Sigma * w)
mvp_vol = np.sqrt(w_mvp.T.dot(cov_matrix).dot(w_mvp))

# 按照输出契约存入字典
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': mvp_vol
}

# 打印结果验证
print(result)
