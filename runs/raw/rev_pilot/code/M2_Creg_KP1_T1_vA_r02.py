import numpy as np

# 输入数据
annual_vol = np.array([0.187, 0.243, 0.312])
corr = np.array([
    [1.00,  0.21, -0.13],
    [0.21,  1.00,  0.37],
    [-0.13, 0.37,  1.00]
])

# 协方差矩阵
cov = np.outer(annual_vol, annual_vol) * corr

# 全局最小方差组合解析解
inv_cov = np.linalg.inv(cov)
ones = np.ones(len(annual_vol))
mvp_weights = inv_cov @ ones / (ones @ inv_cov @ ones)

# 组合年化波动率
var_mvp = 1.0 / (ones @ inv_cov @ ones)
mvp_vol_annual = np.sqrt(var_mvp)

# 结果字典
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol_annual)
}

# 输出结果便于校验
print(result)
