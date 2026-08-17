import numpy as np

# 给定数据
vol1 = 0.187
vol2 = 0.243
vol3 = 0.312
rho12 = 0.21
rho13 = -0.13
rho23 = 0.37

# 构建协方差矩阵
cov12 = rho12 * vol1 * vol2
cov13 = rho13 * vol1 * vol3
cov23 = rho23 * vol2 * vol3

cov_matrix = np.array([
    [vol1**2, cov12, cov13],
    [cov12, vol2**2, cov23],
    [cov13, cov23, vol3**2]
])

# 构建约束矩阵：全投资约束 sum(wi) = 1
A = np.array([[1, 1, 1]])
b = np.array([1])

# 增广矩阵求解最小方差组合
A_full = np.zeros((4, 3))
A_full[0, :] = 1  # 权重和为1
A_full[1, :] = cov_matrix[0, :]
A_full[2, :] = cov_matrix[1, :]
A_full[3, :] = cov_matrix[2, :]

# 使用拉格朗日乘子法解最小方差组合
# 构建左侧矩阵 (4x4)
left = np.zeros((4, 4))
left[0:3, 0:3] = 2 * cov_matrix
left[0:3, 3] = 1
left[3, 0:3] = 1

right = np.array([0, 0, 0, 1])

solution = np.linalg.solve(left, right)
weights = solution[:3]
port_vol = np.sqrt(weights @ cov_matrix @ weights)

# 存储结果
result = {
    'mvp_weights': weights.round(6).tolist(),
    'mvp_vol_annual': round(port_vol, 6)
}
print(result)
