import numpy as np

# 1. 输入数据
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr_matrix = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37,  1.0 ]
])

# 构造协方差矩阵
Sigma = np.outer(vols, vols) * corr_matrix  # 逐元素相乘

# 2. 求全局最小方差组合权重（允许卖空，满仓）
# 闭式解：w = (Σ^{-1} * 1) / (1' * Σ^{-1} * 1)
n = len(vols)
ones = np.ones(n)
Sigma_inv = np.linalg.inv(Sigma)
w_mvp = Sigma_inv @ ones / (ones @ Sigma_inv @ ones)

# 3. 组合波动率
var_mvp = w_mvp @ Sigma @ w_mvp
vol_mvp = np.sqrt(var_mvp)

# 4. 输出结果字典
result = {
    'mvp_weights': w_mvp,
    'mvp_vol_annual': vol_mvp
}

# 打印结果（教师投屏用）
print("全局最小方差组合权重 (w1, w2, w3):")
print(np.round(w_mvp, 6))
print(f"\n年化波动率: {vol_mvp:.6f} ({vol_mvp*100:.4f}%)")
