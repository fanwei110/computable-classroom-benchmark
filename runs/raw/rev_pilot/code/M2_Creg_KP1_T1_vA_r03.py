import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ----- 给定的数据 -----
vol = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr = np.array([
    [1.00, 0.21, -0.13],
    [0.21, 1.00,  0.37],
    [-0.13, 0.37, 1.00]
])

# 构建协方差矩阵 (年化)
cov_matrix = np.outer(vol, vol) * corr

# 全局最小方差组合 (MVP) 的解析解
# 权重 = (Σ^{-1} * 1) / (1^T * Σ^{-1} * 1)
inv_cov = np.linalg.inv(cov_matrix)
ones = np.ones(len(vol))
weights = inv_cov @ ones / (ones @ inv_cov @ ones)

# 计算组合年化波动率
portfolio_variance = weights @ cov_matrix @ weights
portfolio_vol = np.sqrt(portfolio_variance)

# 存储结果
result = {
    'mvp_weights': weights.tolist(),
    'mvp_vol_annual': portfolio_vol
}

# 输出结果供检查
print("全局最小方差组合权重:", result['mvp_weights'])
print("组合年化波动率:", result['mvp_vol_annual'])

# 若需要，可以检验：权重之和为1
print("权重之和:", np.sum(weights))
