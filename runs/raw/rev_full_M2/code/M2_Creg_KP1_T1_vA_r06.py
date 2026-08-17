import numpy as np

# 年化波动率
vol = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr = np.array([
    [1.0,   0.21, -0.13],
    [0.21,  1.0,   0.37],
    [-0.13, 0.37,  1.0]
])

# 计算协方差矩阵
cov = np.diag(vol) @ corr @ np.diag(vol)

# 全局最小方差组合 (允许卖空，资金全部投出，即权重和为1)
inv_cov = np.linalg.inv(cov)
ones = np.ones(len(vol))
mvp_weights = inv_cov @ ones / (ones @ inv_cov @ ones)

# 年化波动率
mvp_vol_annual = np.sqrt(mvp_weights @ cov @ mvp_weights)

# 结果存入字典
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': round(mvp_vol_annual, 10)  # 保持高精度可复现
}

# 打印结果
if __name__ == "__main__":
    print("全局最小方差组合权重:", result['mvp_weights'])
    print("全局最小方差组合年化波动率:", result['mvp_vol_annual'])
