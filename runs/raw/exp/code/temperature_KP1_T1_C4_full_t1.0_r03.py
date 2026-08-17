import numpy as np

# 1. 输入参数
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr_matrix = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 构造协方差矩阵
Sigma = np.outer(vols, vols) * corr_matrix  # 逐元素乘法

# 2. 求全局最小方差组合权重（闭式解，允许卖空，满仓）
# 目标：min w' Σ w  s.t. w'1 = 1
# 解析解：w = (Σ^{-1} 1) / (1' Σ^{-1} 1)

N = len(vols)
ones = np.ones(N)
Sigma_inv = np.linalg.inv(Sigma)
mvp_weights = Sigma_inv @ ones / (ones @ Sigma_inv @ ones)  # 分子分母均为标量

# 3. 计算组合波动率
mvp_var = mvp_weights @ Sigma @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_var)

# 4. 输出结果
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 打印检查（教师投屏时可看到）
print("全局最小方差组合权重：", np.round(mvp_weights, 6))
print("年化波动率：", round(mvp_vol_annual, 6))
