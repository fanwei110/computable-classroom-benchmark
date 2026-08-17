import numpy as np

# ==========================================
# 1. 由波动率与相关系数构造协方差矩阵
# ==========================================
vols = np.array([0.187, 0.243, 0.312])
corr = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37, 1.0 ]
])

# 协方差矩阵 Σ = diag(σ) @ Corr @ diag(σ)
cov_matrix = np.outer(vols, vols) * corr

# ==========================================
# 2. 求最小方差权重（闭式解）
# ==========================================
# 在允许卖空且资金全部投出（Σw_i = 1）的约束下，
# 全局最小方差组合(GMVP)的闭式解为：w = (Σ^-1 * 1) / (1' * Σ^-1 * 1)
ones = np.ones(len(vols))
inv_cov = np.linalg.inv(cov_matrix)

# 计算未归一化的权重
w_unnorm = inv_cov @ ones

# 归一化使其和为1
w_mvp = w_unnorm / np.sum(w_unnorm)

# ==========================================
# 3. 组合波动率取 w'Σw 的平方根
# ==========================================
var_mvp = w_mvp @ cov_matrix @ w_mvp
vol_mvp = np.sqrt(var_mvp)

# ==========================================
# 4. 按要求键名填充 result
# ==========================================
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(vol_mvp)
}

# 打印结果以供验证
print("全局最小方差组合结果：")
print(f"权重分布: {result['mvp_weights']}")
print(f"年化波动率: {result['mvp_vol_annual']:.4f} (即 {result['mvp_vol_annual']*100:.2f}%)")
