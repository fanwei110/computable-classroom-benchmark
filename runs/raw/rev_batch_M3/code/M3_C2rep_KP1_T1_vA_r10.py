import numpy as np

# 1. 由波动率与相关系数构造协方差矩阵
vols = np.array([0.187, 0.243, 0.312])
corr_matrix = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37, 1.0 ]
])

# 协方差矩阵 Σ = diag(σ) @ Corr @ diag(σ)
cov_matrix = np.outer(vols, vols) * corr_matrix

# 2. 求最小方差权重（闭式解：w = Σ^-1 * 1 / (1' * Σ^-1 * 1)）
ones = np.ones(3)
inv_cov = np.linalg.inv(cov_matrix)
w_mvp = (inv_cov @ ones) / (ones @ inv_cov @ ones)

# 3. 组合波动率取 w'Σw 的平方根
port_var = w_mvp @ cov_matrix @ w_mvp
port_vol = np.sqrt(port_var)

# 4. 按要求键名填充 result
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(port_vol)
}

# 供教师投屏验证打印
if __name__ == '__main__':
    print("全局最小方差组合权重:", result['mvp_weights'])
    print("全局最小方差组合年化波动率:", result['mvp_vol_annual'])
