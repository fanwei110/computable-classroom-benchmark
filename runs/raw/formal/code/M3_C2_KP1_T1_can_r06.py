import numpy as np

# ================= 步骤 1：由波动率与相关系数构造协方差矩阵 =================
# 年化波动率
vols = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr = np.array([
    [1.00,  0.21, -0.13],
    [0.21,  1.00,  0.37],
    [-0.13, 0.37,  1.00]
])

# 协方差矩阵: Σ = diag(σ) * C * diag(σ)
cov_matrix = np.outer(vols, vols) * corr

# ================= 步骤 2：求最小方差权重 =================
# 马科维茨全局最小方差组合(MVP)闭式解: w = (Σ^-1 * 1) / (1' * Σ^-1 * 1)
# 其中 1 为全1列向量
ones = np.ones(len(vols))
cov_inv = np.linalg.inv(cov_matrix)

# 计算未归一化的权重
w_unnorm = cov_inv @ ones

# 归一化使权重和为1
mvp_weights = w_unnorm / np.sum(w_unnorm)

# ================= 步骤 3：计算组合年化波动率 =================
# 组合方差: σ_p^2 = w' Σ w
mvp_var = mvp_weights.T @ cov_matrix @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_var)

# ================= 步骤 4：按要求键名填充 result =================
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 打印结果以便课堂展示
print("全局最小方差组合权重:", result['mvp_weights'])
print("全局最小方差组合年化波动率:", result['mvp_vol_annual'])
