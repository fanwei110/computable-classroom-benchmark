import numpy as np

# 1. 定义给定的参数
vols_annual = np.array([0.187, 0.243, 0.312])

corr_12 = 0.21
corr_13 = -0.13
corr_23 = 0.37

# 构建相关系数矩阵
corr_matrix = np.array([
    [1.0,   corr_12, corr_13],
    [corr_12, 1.0,   corr_23],
    [corr_13, corr_23, 1.0  ]
])

# 2. 计算年化协方差矩阵
# Sigma = diag(sigma) @ Corr @ diag(sigma)
cov_matrix = np.outer(vols_annual, vols_annual) * corr_matrix

# 3. 计算全局最小方差组合 (MVP) 的权重
# 公式: w_mvp = (Sigma^-1 @ 1) / (1^T @ Sigma^-1 @ 1)
ones = np.ones(len(vols_annual))
cov_inv = np.linalg.inv(cov_matrix)

# 计算分母: 1^T @ Sigma^-1 @ 1
cov_inv_ones = cov_inv @ ones
denominator = ones @ cov_inv_ones

# 计算 MVP 权重
mvp_weights = cov_inv_ones / denominator

# 4. 计算 MVP 的年化波动率
# MVP 方差公式: sigma_mvp^2 = 1 / (1^T @ Sigma^-1 @ 1)
mvp_var = 1.0 / denominator
mvp_vol_annual = np.sqrt(mvp_var)

# 5. 按照输出契约保存结果
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 打印结果以便验证
if __name__ == "__main__":
    print("全局最小方差组合权重:", result['mvp_weights'])
    print("全局最小方差组合年化波动率:", result['mvp_vol_annual'])
