import numpy as np

# ========== 1. 构造协方差矩阵 ==========
# 年化波动率（标准差）
sigma = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr_matrix = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 协方差矩阵 = diag(sigma) * corr_matrix * diag(sigma)
cov_matrix = np.diag(sigma) @ corr_matrix @ np.diag(sigma)

# ========== 2. 求全局最小方差组合权重 (允许卖空，满仓) ==========
# 闭式解：w_min = (Σ⁻¹ * 1) / (1' * Σ⁻¹ * 1)
inv_cov = np.linalg.inv(cov_matrix)
n = len(sigma)
ones = np.ones(n)

w_min = inv_cov @ ones / (ones @ inv_cov @ ones)

# ========== 3. 组合年化波动率 ==========
portfolio_variance = w_min @ cov_matrix @ w_min
mvp_vol = np.sqrt(portfolio_variance)

# ========== 4. 输出 result 字典 ==========
result = {
    'mvp_weights': w_min,          # 三个权重，ndarray
    'mvp_vol_annual': mvp_vol      # 小数，如0.1763
}

# 打印结果便于课堂展示（保留4位小数）
print("全局最小方差组合权重：")
for i, w in enumerate(w_min, 1):
    print(f"  资产{i}: {w:.6f}")
print(f"\n年化波动率: {mvp_vol:.4%}")

# 验证权重和为1
print(f"\n权重和: {w_min.sum():.8f}")
