import numpy as np

# 年化波动率
sigmas = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr = np.array([
    [ 1.00,  0.21, -0.13],
    [ 0.21,  1.00,  0.37],
    [-0.13,  0.37,  1.00]
])

# 1. 构造协方差矩阵
cov = np.outer(sigmas, sigmas) * corr

# 2. 全局最小方差组合权重（允许卖空，满仓）
ones = np.ones(3)
inv_cov = np.linalg.inv(cov)
w_mvp = inv_cov @ ones / (ones @ inv_cov @ ones)

# 3. 组合年化波动率
mvp_vol = np.sqrt(w_mvp @ cov @ w_mvp)

# 输出结果
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': mvp_vol
}

if __name__ == "__main__":
    print(result)
