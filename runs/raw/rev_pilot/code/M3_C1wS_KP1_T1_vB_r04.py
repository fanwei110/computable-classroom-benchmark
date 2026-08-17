import numpy as np

# ==================== 1. 构造协方差矩阵 ====================
# 给定波动率与相关系数
vols = np.array([0.187, 0.243, 0.312])
corr_matrix = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37, 1.0 ]
])

# 协方差矩阵 Σ = diag(σ) @ Corr @ diag(σ) 等价于 outer(σ, σ) * Corr
cov_matrix = np.outer(vols, vols) * corr_matrix

# ==================== 2. 求最小方差权重 ====================
# 在仅有满仓约束（Σw = 1）且允许做空的情况下，最小方差组合的闭式解为：
# w_mvp = Σ^-1 @ 1 / (1^T @ Σ^-1 @ 1)
inv_cov = np.linalg.inv(cov_matrix)
ones = np.ones(len(vols))

w_mvp = (inv_cov @ ones) / (ones.T @ inv_cov @ ones)

# ==================== 3. 计算组合波动率 ====================
# 组合方差 σ_p^2 = w^T @ Σ @ w，组合波动率取其平方根
mvp_var = w_mvp.T @ cov_matrix @ w_mvp
mvp_vol = np.sqrt(mvp_var)

# ==================== 4. 填充结果字典 ====================
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': mvp_vol.item()
}

# 投屏展示输出
print("--- 最小方差组合计算结果 ---")
print(f"资产权重: {result['mvp_weights']}")
print(f"组合年化波动率: {result['mvp_vol_annual']:.4%}")
