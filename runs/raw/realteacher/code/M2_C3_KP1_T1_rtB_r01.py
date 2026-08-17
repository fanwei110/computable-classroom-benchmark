import numpy as np

# 给定数据
vol1 = 0.187
vol2 = 0.243
vol3 = 0.312
rho12 = 0.21
rho13 = -0.13
rho23 = 0.37

# 计算协方差矩阵
cov12 = rho12 * vol1 * vol2
cov13 = rho13 * vol1 * vol3
cov23 = rho23 * vol2 * vol3

var1 = vol1**2
var2 = vol2**2
var3 = vol3**2

# 协方差矩阵
cov_matrix = np.array([
    [var1, cov12, cov13],
    [cov12, var2, cov23],
    [cov13, cov23, var3]
])

# 求最小方差组合权重
# 对于允许卖空且资金全部投出的情况，最小方差组合权重公式：
# w = (Σ^{-1} * 1) / (1^T * Σ^{-1} * 1)

inv_cov = np.linalg.inv(cov_matrix)
ones = np.ones(3)

# 分子
numerator = inv_cov @ ones
# 分母
denominator = ones @ inv_cov @ ones

weights = numerator / denominator

# 计算组合波动率（方差，然后开方）
portfolio_variance = weights @ cov_matrix @ weights
portfolio_vol = np.sqrt(portfolio_variance)

# 结果
result = {
    'mvp_weights': weights.tolist(),
    'mvp_vol_annual': portfolio_vol
}

print(result)
