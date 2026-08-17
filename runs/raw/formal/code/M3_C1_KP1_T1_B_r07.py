import numpy as np

# 已知输入
vol = np.array([0.187, 0.243, 0.312])
rho12, rho13, rho23 = 0.21, -0.13, 0.37

# 构建协方差矩阵
cov12 = rho12 * vol[0] * vol[1]
cov13 = rho13 * vol[0] * vol[2]
cov23 = rho23 * vol[1] * vol[2]

cov_matrix = np.array([
    [vol[0]**2, cov12, cov13],
    [cov12, vol[1]**2, cov23],
    [cov13, cov23, vol[2]**2]
])

# 最小方差组合（允许做空，全投资）解析解公式推导：
# 目标函数 min w^T Σ w, 约束 1^T w = 1
# 拉格朗日函数 L = w^T Σ w - λ(1^T w - 1)
# 对w求导得 2Σw - λ1 = 0 => w = (λ/2) Σ^{-1} 1
# 代入约束 1^T w = 1 => (λ/2) 1^T Σ^{-1} 1 = 1 => λ/2 = 1 / (1^T Σ^{-1} 1)
# 因此 w = Σ^{-1} 1 / (1^T Σ^{-1} 1)

ones = np.ones(3)
cov_inv = np.linalg.inv(cov_matrix)

# 计算权重
w_mvp = cov_inv @ ones / (ones @ cov_inv @ ones)

# 计算组合波动率
port_var = w_mvp @ cov_matrix @ w_mvp
port_vol = np.sqrt(port_var)

# 转换为百分比格式存储
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': port_vol
}

print(result)
