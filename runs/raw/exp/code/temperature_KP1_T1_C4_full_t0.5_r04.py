import numpy as np
import pandas as pd
from scipy.optimize import minimize

# ---------- 1. 构造协方差矩阵 ----------
# 年化波动率
vol = np.array([0.187, 0.243, 0.312])
# 相关系数矩阵
corr = np.array([
    [1.0,   0.21, -0.13],
    [0.21,  1.0,   0.37],
    [-0.13, 0.37,  1.0]
])
# 协方差矩阵 = diag(vol) @ corr @ diag(vol)
cov = np.diag(vol) @ corr @ np.diag(vol)

# ---------- 2. 求全局最小方差组合权重 (允许卖空，满仓) ----------
# 闭式解：w = Σ^{-1} * 1 / (1' Σ^{-1} 1)
n = cov.shape[0]
ones = np.ones(n)
inv_cov = np.linalg.inv(cov)
mvp_weights = inv_cov @ ones / (ones @ inv_cov @ ones)

# ---------- 3. 组合年化波动率 ----------
mvp_var = mvp_weights @ cov @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_var)

# ---------- 4. 输出 result 字典 ----------
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 打印结果（教师投屏可见）
print("全局最小方差组合权重 (w1, w2, w3):")
print(np.round(mvp_weights, 6))
print(f"\n年化波动率: {mvp_vol_annual:.6f} ({mvp_vol_annual*100:.2f}%)")
