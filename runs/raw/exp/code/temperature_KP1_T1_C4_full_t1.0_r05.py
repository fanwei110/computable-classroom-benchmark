import numpy as np

# 步骤1：构造协方差矩阵
vol = np.array([0.187, 0.243, 0.312])
corr_matrix = np.array([
    [1.0,   0.21, -0.13],
    [0.21,  1.0,   0.37],
    [-0.13, 0.37,  1.0 ]
])

# 协方差 = 波动率 * 相关系数 * 波动率 (外积)
cov_matrix = np.outer(vol, vol) * corr_matrix

# 步骤2：求全局最小方差组合权重（闭式解，允许卖空）
# 满仓约束：w1 + w2 + w3 = 1
# 最小化 w' Σ w
# 解析解：w = (Σ^{-1} * 1) / (1' * Σ^{-1} * 1)
n = cov_matrix.shape[0]
one_vector = np.ones(n)
inv_cov = np.linalg.inv(cov_matrix)
weights = inv_cov @ one_vector / (one_vector @ inv_cov @ one_vector)

# 步骤3：计算组合年化波动率
portfolio_variance = weights @ cov_matrix @ weights
portfolio_vol = np.sqrt(portfolio_variance)

# 步骤4：按照要求的键名输出结果
result = {
    'mvp_weights': weights,          # array([..., ..., ...])
    'mvp_vol_annual': portfolio_vol  # 小数形式，如0.1287
}

# 显示结果（教师投屏可见）
print("全局最小方差组合权重 (小数形式):")
print(f"  资产1: {weights[0]:.6f}")
print(f"  资产2: {weights[1]:.6f}")
print(f"  资产3: {weights[2]:.6f}")
print(f"  权重和: {np.sum(weights):.8f} (应接近1)")
print(f"组合年化波动率: {portfolio_vol:.6f} (即 {portfolio_vol*100:.2f}%)")
