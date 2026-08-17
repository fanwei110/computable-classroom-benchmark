import numpy as np
import pandas as pd

# ---------- 1. 构造协方差矩阵 ----------
# 年化波动率
vol = np.array([0.187, 0.243, 0.312])
# 相关系数矩阵
corr = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37,  1.0]
])
# 协方差矩阵 = diag(vol) * corr * diag(vol)
cov = np.diag(vol) @ corr @ np.diag(vol)

# ---------- 2. 求全局最小方差组合权重（闭式解） ----------
# 满仓约束下最小方差组合：w = Σ^{-1} * 1 / (1' Σ^{-1} 1)
n = len(vol)
ones = np.ones(n)
cov_inv = np.linalg.inv(cov)
mvp_weights = cov_inv @ ones / (ones @ cov_inv @ ones)

# ---------- 3. 组合年化波动率 ----------
mvp_var = mvp_weights @ cov @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_var)

# ---------- 4. 按要求填充 result ----------
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 打印结果（教师投屏用）
print("全局最小方差组合权重 (mvp_weights):")
print(np.round(mvp_weights, 6))
print(f"\n年化波动率 (mvp_vol_annual): {mvp_vol_annual:.6f}  ({mvp_vol_annual*100:.4f}%)")
