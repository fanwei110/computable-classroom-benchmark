import numpy as np

# 1. 定义波动率与相关系数（小数表示）
vols = np.array([0.187, 0.243, 0.312])
corr = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37, 1.0 ]
])

# 2. 由波动率与相关系数构造协方差矩阵 Σ
# Σ_ij = ρ_ij * σ_i * σ_j
cov_matrix = np.outer(vols, vols) * corr

# 3. 求全局最小方差组合（MVP）权重
# 闭式解：w_mvp = (Σ^-1 * 1) / (1' * Σ^-1 * 1)
# 其中 1 为全1列向量
cov_inv = np.linalg.inv(cov_matrix)
ones = np.ones(3)

# Σ^-1 * 1
cov_inv_ones = cov_inv @ ones

# 分母 1' * Σ^-1 * 1
denominator = ones @ cov_inv_ones

# 归一化使其和为 1
mvp_weights = cov_inv_ones / denominator

# 4. 计算组合波动率：sqrt(w'Σw)
mvp_var = mvp_weights @ cov_matrix @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_var)

# 5. 按要求键名填充 result 字典
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': mvp_vol_annual
}

# 投屏展示结果
if __name__ == '__main__':
    print("全局最小方差组合结果：")
    print(f"权重 (mvp_weights): {result['mvp_weights']}")
    print(f"年化波动率 (mvp_vol_annual): {result['mvp_vol_annual']:.6f}")
