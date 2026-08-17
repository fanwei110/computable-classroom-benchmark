import numpy as np
import pandas as pd
from scipy.optimize import minimize

# ---------- 1. 输入数据 ----------
# 年化波动率（小数）
vol1 = 0.187
vol2 = 0.243
vol3 = 0.312

# 相关系数矩阵
corr_matrix = np.array([
    [1.0,   0.21, -0.13],
    [0.21,  1.0,   0.37],
    [-0.13, 0.37,  1.0 ]
])

# 标准差向量
sigma = np.array([vol1, vol2, vol3])

# ---------- 2. 构造协方差矩阵 ----------
# 协方差矩阵 = diag(sigma) * corr_matrix * diag(sigma)
Sigma = np.diag(sigma) @ corr_matrix @ np.diag(sigma)

# ---------- 3. 求全局最小方差组合权重（闭式解） ----------
# 满仓约束：w1 + w2 + w3 = 1，允许卖空
# 闭式解：w_min = (Σ⁻¹ * 1) / (1' * Σ⁻¹ * 1)
n = 3
one_vector = np.ones(n)
Sigma_inv = np.linalg.inv(Sigma)
w_mvp = Sigma_inv @ one_vector / (one_vector @ Sigma_inv @ one_vector)

# ---------- 4. 计算组合年化波动率 ----------
# 组合方差 = w' Σ w
var_mvp = w_mvp @ Sigma @ w_mvp
vol_mvp = np.sqrt(var_mvp)

# ---------- 5. 输出结果 ----------
result = {
    'mvp_weights': w_mvp,           # numpy array, 小数
    'mvp_vol_annual': vol_mvp       # 小数，如 0.15 表示 15%
}

# 显示结果（教师投屏用）
print("全局最小方差组合权重 (w1, w2, w3):")
print(np.round(w_mvp, 6))
print(f"组合年化波动率: {vol_mvp:.6f} ({vol_mvp*100:.2f}%)")
