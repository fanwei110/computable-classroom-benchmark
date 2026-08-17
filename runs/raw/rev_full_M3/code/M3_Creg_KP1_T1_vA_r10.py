import numpy as np

# ==================== 数据输入 ====================
# 三只资产的年化波动率
vol_annual = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr = np.array([
    [1.00, 0.21, -0.13],
    [0.21, 1.00, 0.37],
    [-0.13, 0.37, 1.00]
])

# ==================== 协方差矩阵构建 ====================
# 协方差矩阵 Σ = diag(σ) @ C @ diag(σ)，等价于外积逐元素乘相关系数矩阵
cov_matrix = np.outer(vol_annual, vol_annual) * corr

# ==================== 全局最小方差组合 (MVP) 计算 ====================
ones = np.ones(3)

# 求解协方差矩阵的逆矩阵
cov_inv = np.linalg.inv(cov_matrix)

# 计算 MVP 权重: w = Σ^-1 * 1 / (1^T * Σ^-1 * 1)
mvp_weights = (cov_inv @ ones) / (ones.T @ cov_inv @ ones)

# 计算 MVP 方差: σ^2 = 1 / (1^T * Σ^-1 * 1)
mvp_var = 1.0 / (ones.T @ cov_inv @ ones)

# 计算 MVP 年化波动率
mvp_vol_annual = np.sqrt(mvp_var)

# ==================== 结果输出 ====================
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 打印结果以供验证
if __name__ == "__main__":
    print("全局最小方差组合权重:")
    for i, w in enumerate(result['mvp_weights']):
        print(f"  资产 {i+1}: {w:.4%}")
    print(f"全局最小方差组合年化波动率: {result['mvp_vol_annual']:.4%}")
