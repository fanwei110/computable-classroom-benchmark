import numpy as np

# ==================== 1. 由波动率与相关系数构造协方差矩阵 ====================
# 给定的年化波动率
vols = np.array([0.187, 0.243, 0.312])

# 给定的相关系数矩阵
corr_matrix = np.array([
    [1.00,  0.21, -0.13],
    [0.21,  1.00,  0.37],
    [-0.13, 0.37,  1.00]
])

# 协方差矩阵 Σ = diag(σ) @ Corr @ diag(σ) 
# 等价于 Σ_ij = σ_i * σ_j * ρ_ij
cov_matrix = np.outer(vols, vols) * corr_matrix

# ==================== 2. 求最小方差权重 ====================
# 满仓约束下，全局最小方差组合(MVP)的闭式解为：w_mvp = (Σ^-1 @ 1) / (1' @ Σ^-1 @ 1)
# 其中 1 为全1列向量
inv_cov = np.linalg.inv(cov_matrix)
ones = np.ones(3)

# 计算未归一化的权重
raw_weights = inv_cov @ ones

# 归一化使其和为 1
mvp_weights = raw_weights / np.sum(raw_weights)

# ==================== 3. 计算组合年化波动率 ====================
# 组合方差为 w'Σw，波动率为其平方根
mvp_var = mvp_weights @ cov_matrix @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_var)

# ==================== 4. 按要求键名填充 result ====================
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol_annual)
}

# --- 课堂投屏展示辅助打印 ---
print("=== 马科维茨全局最小方差组合计算 ===")
print(f"协方差矩阵:\n{np.round(cov_matrix, 6)}\n")
print(f"MVP权重   : [{', '.join([f'{w:.4f}' for w in result['mvp_weights']])}]")
print(f"权重之和  : {sum(result['mvp_weights']):.6f}")
print(f"MVP年化波动率: {result['mvp_vol_annual']:.4f} ({result['mvp_vol_annual']*100:.2f}%)")
print("=====================================")

