import numpy as np

# 1. 定义输入参数
vols_annual = np.array([0.187, 0.243, 0.312])
corr_matrix = np.array([
    [1.0,   0.21, -0.13],
    [0.21,  1.0,   0.37],
    [-0.13, 0.37,  1.0 ]
])

# 2. 构建协方差矩阵
# cov(i,j) = corr(i,j) * vol_i * vol_j
cov_matrix = np.outer(vols_annual, vols_annual) * corr_matrix

# 3. 计算全局最小方差组合 (MVP) 的权重
# 公式: w_mvp = (Sigma^-1 * 1) / (1^T * Sigma^-1 * 1)
ones = np.ones(3)
inv_cov = np.linalg.inv(cov_matrix)

w_unnorm = inv_cov @ ones
w_mvp = w_unnorm / np.sum(w_unnorm)

# 4. 计算 MVP 的年化波动率
# 公式: sigma_mvp = sqrt(w_mvp^T * Sigma * w_mvp)
var_mvp = w_mvp.T @ cov_matrix @ w_mvp
vol_mvp = np.sqrt(var_mvp)

# 5. 按照输出契约存入字典
result = {
    'mvp_weights': w_mvp,
    'mvp_vol_annual': vol_mvp
}

# (可选) 打印结果以供直观检查
if __name__ == "__main__":
    print("全局最小方差组合权重:", result['mvp_weights'])
    print("全局最小方差组合年化波动率:", result['mvp_vol_annual'])
