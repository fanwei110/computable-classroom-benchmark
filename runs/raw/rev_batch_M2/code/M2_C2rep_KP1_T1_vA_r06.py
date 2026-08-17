import numpy as np

# 给定数据
sigma = np.array([0.187, 0.243, 0.312])  # 年化波动率

# 相关系数矩阵（下三角给出，构造对称矩阵）
rho = np.array([
    [1.00,  0.21, -0.13],
    [0.21,  1.00,  0.37],
    [-0.13, 0.37,  1.00]
])

# 1. 构造协方差矩阵
# Σ[i,j] = ρ[i,j] * σ[i] * σ[j]
cov_matrix = np.outer(sigma, sigma) * rho

# 2. 计算全局最小方差组合权重（允许卖空，权重和=1）
# 闭式解: w = Σ^{-1} 1 / (1^T Σ^{-1} 1)
inv_cov = np.linalg.inv(cov_matrix)
ones = np.ones(3)
w_unnormalized = inv_cov @ ones   # 等同于 inv_cov.dot(ones)
denom = ones @ w_unnormalized     # 1^T Σ^{-1} 1
weights = w_unnormalized / denom  # 归一化使其和为1

# 3. 组合方差与年化波动率
port_variance = weights @ cov_matrix @ weights   # w' Σ w
port_vol_annual = np.sqrt(port_variance)

# 4. 构造输出字典
result = {
    'mvp_weights': weights.tolist(),    # 转换为列表，便于查看
    'mvp_vol_annual': float(port_vol_annual)
}

# 输出结果（课堂投屏用）
print("全局最小方差组合结果：")
print(result)

# 可选：更友好的显示
print("\n权重 (w1, w2, w3):", result['mvp_weights'])
print("年化波动率:", result['mvp_vol_annual'])
