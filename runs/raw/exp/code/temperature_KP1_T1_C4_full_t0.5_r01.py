import numpy as np
import pandas as pd
from scipy.optimize import minimize

# ---------- 1. 输入数据 ----------
# 年化波动率（小数）
vol_1 = 0.187
vol_2 = 0.243
vol_3 = 0.312

# 相关系数矩阵（对称）
corr_matrix = np.array([
    [1.0,   0.21, -0.13],
    [0.21,  1.0,   0.37],
    [-0.13, 0.37,  1.0 ]
])

# 构造协方差矩阵：Σ = diag(σ) * Corr * diag(σ)
sigma = np.array([vol_1, vol_2, vol_3])
Sigma = np.diag(sigma) @ corr_matrix @ np.diag(sigma)

# ---------- 2. 求解全局最小方差组合（允许卖空，满仓） ----------
# 闭式解：w_min = Σ^{-1} * 1 / (1' Σ^{-1} 1)
n = 3
ones = np.ones(n)
Sigma_inv = np.linalg.inv(Sigma)
w_mvp = Sigma_inv @ ones / (ones @ Sigma_inv @ ones)

# ---------- 3. 组合年化波动率 ----------
var_mvp = w_mvp @ Sigma @ w_mvp
vol_mvp = np.sqrt(var_mvp)  # 已经是年化（因为输入波动率是年化的）

# ---------- 4. 输出 result ----------
result = {
    'mvp_weights': w_mvp,          # array([w1, w2, w3])
    'mvp_vol_annual': vol_mvp      # 小数，如 0.1523
}

# 打印结果（教师投屏用）
print("全局最小方差组合权重（小数）：")
print(f"  资产1: {w_mvp[0]:.6f}")
print(f"  资产2: {w_mvp[1]:.6f}")
print(f"  资产3: {w_mvp[2]:.6f}")
print(f"  权重和: {w_mvp.sum():.8f}")
print(f"\n年化组合波动率（小数）: {vol_mvp:.6f}  ({vol_mvp*100:.2f}%)")

# 验证协方差矩阵
print("\n协方差矩阵：")
print(pd.DataFrame(Sigma, 
                   index=['资产1','资产2','资产3'], 
                   columns=['资产1','资产2','资产3']))
