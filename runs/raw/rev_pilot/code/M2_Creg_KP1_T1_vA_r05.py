import numpy as np

# 给定数据：年化波动率
vols = np.array([0.187, 0.243, 0.312])

# 给定相关系数矩阵（下三角部分已对称）
corr = np.array([
    [1.00,  0.21, -0.13],
    [0.21,  1.00,  0.37],
    [-0.13, 0.37,  1.00]
])

# 计算协方差矩阵
cov = np.outer(vols, vols) * corr

# 全局最小方差组合（允许卖空，权重和为1）
inv_cov = np.linalg.inv(cov)
ones = np.ones(3)
w = inv_cov @ ones / (ones @ inv_cov @ ones)

# 组合年化波动率
port_var = w @ cov @ w
port_vol = np.sqrt(port_var)

# 按要求存入字典
result = {
    'mvp_weights': w.tolist(),
    'mvp_vol_annual': port_vol
}

print(result)
