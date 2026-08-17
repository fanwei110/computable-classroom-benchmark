import numpy as np
from scipy.optimize import minimize

# 1. 构造协方差矩阵
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr_matrix = np.array([
    [1.00, 0.21, -0.13],
    [0.21, 1.00,  0.37],
    [-0.13, 0.37, 1.00]
])

# 协方差矩阵 = 波动率对角阵 @ 相关系数矩阵 @ 波动率对角阵
cov_matrix = np.diag(vols) @ corr_matrix @ np.diag(vols)

# 2. 求最小方差组合权重（闭式解）
# 最小方差组合权重 w = (Σ⁻¹ @ 1) / (1' @ Σ⁻¹ @ 1)
ones = np.ones(3)
inv_cov = np.linalg.inv(cov_matrix)
mvp_weights = inv_cov @ ones / (ones.T @ inv_cov @ ones)
mvp_weights = mvp_weights.flatten()  # 确保是一维数组

# 3. 计算组合波动率
mvp_vol_annual = np.sqrt(mvp_weights.T @ cov_matrix @ mvp_weights)

# 4. 填充结果字典
result = {
    'mvp_weights': mvp_weights.tolist(),  # 转为列表以确保 JSON 可序列化
    'mvp_vol_annual': float(mvp_vol_annual)  # 转为 Python float
}

# 打印结果以供验证（非必须，但便于调试）
print(result)
