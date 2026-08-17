import numpy as np

# ================= 步骤 1：设定参数并构造协方差矩阵 =================
# 年化波动率
vols = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr_matrix = np.array([
    [1.00,  0.21, -0.13],
    [0.21,  1.00,  0.37],
    [-0.13, 0.37,  1.00]
])

# 协方差矩阵 Σ = D * Corr * D，其中 D 为波动率对角阵
# 等价于 np.outer(vols, vols) * corr_matrix
cov_matrix = np.outer(vols, vols) * corr_matrix

# ================= 步骤 2：求解全局最小方差组合权重 =================
# 满仓且允许卖空约束下，MVP闭式解为：w_mvp = Σ^-1 * 1 / (1^T * Σ^-1 * 1)
inv_cov = np.linalg.inv(cov_matrix)
ones = np.ones(len(vols))

# 计算 Σ^-1 * 1
inv_cov_ones = inv_cov @ ones

# 归一化，使权重之和为1
mvp_weights = inv_cov_ones / np.sum(inv_cov_ones)

# ================= 步骤 3：计算组合年化波动率 =================
# 组合方差 w'Σw，波动率取其平方根
mvp_var = mvp_weights.T @ cov_matrix @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_var)

# ================= 步骤 4：按要求填充结果 =================
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol_annual)
}

# （可选）课堂投屏展示打印
if __name__ == '__main__':
    print("全局最小方差组合权重:", result['mvp_weights'])
    print("权重之和:", sum(result['mvp_weights']))
    print("全局最小方差组合年化波动率:", result['mvp_vol_annual'])
