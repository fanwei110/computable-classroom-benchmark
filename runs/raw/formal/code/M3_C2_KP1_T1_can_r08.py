import numpy as np

# ==================== 1. 构造协方差矩阵 ====================
# 已知年化波动率
vols_annual = np.array([0.187, 0.243, 0.312])

# 已知相关系数矩阵
corr_matrix = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37, 1.0 ]
])

# 协方差矩阵 Σ = diag(σ) @ Corr @ diag(σ)
diag_vols = np.diag(vols_annual)
cov_matrix = diag_vols @ corr_matrix @ diag_vols

# ==================== 2. 求最小方差权重 ====================
# 允许卖空且资金全部投出（权重之和为1），全局最小方差组合(MVP)闭式解为：
# w_mvp = Σ^(-1) @ 1 / (1^T @ Σ^(-1) @ 1)
ones_vector = np.ones(3)
cov_inv = np.linalg.inv(cov_matrix)

# 计算权重
mvp_weights = (cov_inv @ ones_vector) / (ones_vector.T @ cov_inv @ ones_vector)

# ==================== 3. 计算组合波动率 ====================
# 组合方差 = w'Σw，组合波动率 = sqrt(w'Σw)
mvp_variance = mvp_weights.T @ cov_matrix @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_variance)

# ==================== 4. 填充结果字典 ====================
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': mvp_vol_annual
}

# ------------------- 课堂展示输出 -------------------
print("="*50)
print("马科维茨均值-方差组合理论 - 全局最小方差组合计算")
print("="*50)
print(f"资产年化波动率: {vols_annual.tolist()}")
print(f"资产相关系数矩阵:\n{corr_matrix}")
print("-"*50)
print(f"全局最小方差组合权重: {result['mvp_weights']}")
print(f"权重之和(验证满仓约束): {sum(result['mvp_weights']):.6f}")
print(f"全局最小方差组合年化波动率: {result['mvp_vol_annual']:.4%}")
print("="*50)
