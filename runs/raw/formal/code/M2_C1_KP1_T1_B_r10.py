import numpy as np

# 给定数据
vol = np.array([0.187, 0.243, 0.312])
rho = np.array([[1.0, 0.21, -0.13],
                [0.21, 1.0, 0.37],
                [-0.13, 0.37, 1.0]])

# 协方差矩阵
Sigma = np.outer(vol, vol) * rho

# 最小方差组合（允许做空，全额投资）
ones = np.ones(3)
Sigma_inv = np.linalg.inv(Sigma)
w_raw = Sigma_inv @ ones
w_mvp = w_raw / np.sum(w_raw)

# 组合年化波动率
mvp_var = w_mvp @ Sigma @ w_mvp
mvp_vol = np.sqrt(mvp_var)

result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': float(mvp_vol)
}

print(result)
