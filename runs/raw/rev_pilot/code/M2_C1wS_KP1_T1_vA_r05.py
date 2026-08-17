import numpy as np

# 年化波动率
sigma = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13,0.37,  1.0 ]
])

# 1. 构造协方差矩阵
Sigma = np.outer(sigma, sigma) * corr

# 2. 求最小方差权重 (允许卖空，满仓)
ones = np.ones(3)
inv_Sigma = np.linalg.inv(Sigma)
w_unscaled = inv_Sigma @ ones
w_mvp = w_unscaled / np.sum(w_unscaled)   # 权重和归一化为1

# 3. 组合年化波动率
mvp_vol = np.sqrt(w_mvp @ Sigma @ w_mvp)

# 4. 输出字典
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(mvp_vol)
}

# 打印结果以便课堂展示
print("最小方差组合权重:", result['mvp_weights'])
print("组合年化波动率:", result['mvp_vol_annual'])
