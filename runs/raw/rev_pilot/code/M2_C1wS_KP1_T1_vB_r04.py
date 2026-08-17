import numpy as np

# 给定数据
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
rho12 = 0.21
rho13 = -0.13
rho23 = 0.37

# 构建相关系数矩阵
corr = np.array([
    [1.0, rho12, rho13],
    [rho12, 1.0, rho23],
    [rho13, rho23, 1.0]
])

# 构建协方差矩阵
Sigma = np.diag(vols) @ corr @ np.diag(vols)

# 计算最小方差组合权重（允许做空，权重和为1）
n = len(vols)
ones = np.ones(n)
inv_Sigma = np.linalg.inv(Sigma)
w_mvp = inv_Sigma @ ones / (ones @ inv_Sigma @ ones)

# 计算组合波动率
vol_mvp = np.sqrt(w_mvp @ Sigma @ w_mvp)

# 填充结果
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(vol_mvp)
}

# 打印结果
print(result)
