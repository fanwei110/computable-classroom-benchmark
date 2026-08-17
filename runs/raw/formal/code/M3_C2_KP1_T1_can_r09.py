import numpy as np

# ==================== 1. 由波动率与相关系数构造协方差矩阵 ====================
# 年化波动率
vols = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37, 1.0 ]
])

# 协方差矩阵 Σ = diag(σ) @ Corr @ diag(σ)
cov_matrix = np.diag(vols) @ corr @ np.diag(vols)

# ==================== 2. 求最小方差权重 ====================
# 全局最小方差组合(MVP)闭式解：w_mvp = (Σ^-1 @ 1) / (1^T @ Σ^-1 @ 1)
ones = np.ones(3)
inv_cov = np.linalg.inv(cov_matrix)

# 计算权重并归一化（公式本身已保证权重和为1）
mvp_weights = (inv_cov @ ones) / (ones.T @ inv_cov @ ones)

# ==================== 3. 组合波动率取 w'Σw 的平方根 ====================
# 组合方差
mvp_var = mvp_weights.T @ cov_matrix @ mvp_weights
# 组合年化波动率
mvp_vol_annual = np.sqrt(mvp_var)

# ==================== 4. 按要求键名填充 result ====================
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol_annual)
}

# (投屏演示时可用于打印验证)
# print(f"全局最小方差组合权重: {result['mvp_weights']}")
# print(f"全局最小方差组合年化波动率: {result['mvp_vol_annual']:.4%}")
