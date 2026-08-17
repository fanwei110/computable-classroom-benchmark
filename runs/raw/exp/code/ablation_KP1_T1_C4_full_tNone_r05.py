import numpy as np
import pandas as pd
import scipy.optimize as sco

# ---------- 1. 构造协方差矩阵 ----------
# 年化波动率
vols = np.array([0.187, 0.243, 0.312])
# 相关系数矩阵
corr_matrix = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])
# 协方差矩阵 = 对角阵(vols) * corr * 对角阵(vols)
cov_matrix = np.diag(vols) @ corr_matrix @ np.diag(vols)

# ---------- 2. 求全局最小方差权重 ----------
# 闭式解：w = Σ⁻¹ 1 / (1' Σ⁻¹ 1)
n = len(vols)
ones = np.ones(n)
inv_cov = np.linalg.inv(cov_matrix)
mvp_weights = inv_cov @ ones / (ones @ inv_cov @ ones)

# ---------- 3. 组合波动率 ----------
mvp_var = mvp_weights @ cov_matrix @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_var)

# ---------- 4. 按要求输出 ----------
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 显示结果
print("全局最小方差组合权重 (三只资产):", result['mvp_weights'])
print("年化波动率:", f"{result['mvp_vol_annual']:.6f}")
