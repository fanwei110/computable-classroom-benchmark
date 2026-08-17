import numpy as np

# ==================== 1. 定义输入参数 ====================
# 年化波动率
vols_annual = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr_matrix = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37, 1.0 ]
])

# ==================== 2. 构造协方差矩阵 ====================
# 公式: Σ = diag(σ) @ Corr @ diag(σ)，等价于 σ_i * σ_j * ρ_ij
cov_matrix = np.outer(vols_annual, vols_annual) * corr_matrix

# ==================== 3. 求全局最小方差组合权重 ====================
# 马科维茨满仓允许卖空约束下的GMV闭式解: w_mvp = (Σ^-1 * 1) / (1^T * Σ^-1 * 1)
ones = np.ones(len(vols_annual))
inv_cov = np.linalg.inv(cov_matrix)

# 计算逆矩阵与全1向量的乘积
inv_cov_ones = inv_cov @ ones

# 归一化，使权重和为1
w_mvp = inv_cov_ones / np.sum(inv_cov_ones)

# ==================== 4. 计算组合年化波动率 ====================
# 组合方差: σ_p^2 = w^T Σ w
# 组合波动率: σ_p = sqrt(σ_p^2)
var_mvp = w_mvp @ cov_matrix @ w_mvp
vol_mvp = np.sqrt(var_mvp)

# ==================== 5. 填充输出结果 ====================
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(vol_mvp)
}

# 课堂投屏展示
print("="*50)
print("马科维茨均值-方差组合理论 - 全局最小方差组合计算")
print("="*50)
print(f"协方差矩阵:\n{cov_matrix}\n")
print(f"最小方差组合权重: {result['mvp_weights']}")
print(f"权重之和: {sum(result['mvp_weights']):.4f}")
print(f"最小方差组合年化波动率: {result['mvp_vol_annual']:.4%}")
print("="*50)
