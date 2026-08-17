import numpy as np

# ==================== 1. 设定已知参数 ====================
# 三只风险资产的年化波动率
vols = np.array([0.187, 0.243, 0.312])

# 相关系数（矩阵形式，对角线为1）
corr_matrix = np.array([
    [1.0,   0.21, -0.13],
    [0.21,  1.0,   0.37],
    [-0.13, 0.37,  1.0 ]
])

# ==================== 2. 构造协方差矩阵 ====================
# 协方差矩阵 Σ = diag(σ) @ C @ diag(σ)
D = np.diag(vols)
cov_matrix = D @ corr_matrix @ D

# ==================== 3. 计算全局最小方差组合权重 ====================
# 满仓约束下（Σw_i = 1），允许卖空时，MVP的闭式解为：
# w_mvp = (Σ^-1 * 1) / (1^T * Σ^-1 * 1)
ones = np.ones(3)
inv_cov = np.linalg.inv(cov_matrix)

# 计算未归一化的权重
w_unnorm = inv_cov @ ones

# 归一化使权重和为1
w_mvp = w_unnorm / np.sum(w_unnorm)

# ==================== 4. 计算组合年化波动率 ====================
# 组合方差 σ_p^2 = w'Σw
var_portfolio = w_mvp.T @ cov_matrix @ w_mvp

# 组合年化波动率 σ_p = sqrt(w'Σw)
vol_portfolio = np.sqrt(var_portfolio)

# ==================== 5. 填充输出契约 ====================
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(vol_portfolio)
}

# （可选）课堂打印展示
if __name__ == '__main__':
    print("全局最小方差组合权重:", result['mvp_weights'])
    print("全局最小方差组合年化波动率:", result['mvp_vol_annual'])
