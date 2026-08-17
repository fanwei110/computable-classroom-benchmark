import numpy as np

# ==================== 1. 参数设定 ====================
# 三只风险资产的年化波动率（小数表示）
vols = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr = np.array([
    [1.00,  0.21, -0.13],
    [0.21,  1.00,  0.37],
    [-0.13, 0.37,  1.00]
])

# ==================== 2. 构造协方差矩阵 ====================
# 协方差矩阵 Σ = diag(σ) @ Corr @ diag(σ) 等价于外积逐元素相乘
cov_matrix = np.outer(vols, vols) * corr

# ==================== 3. 求全局最小方差组合权重 ====================
# 在允许卖空且满仓约束（权重和为1）下，最小方差组合权重的闭式解为：
# w_mvp = Σ^{-1} * 1 / (1' * Σ^{-1} * 1)
ones = np.ones(3)
cov_inv = np.linalg.inv(cov_matrix)
w_mvp = cov_inv @ ones / (ones @ cov_inv @ ones)

# ==================== 4. 计算组合年化波动率 ====================
# 组合方差为 w'Σw，组合波动率取其平方根
port_var = w_mvp.T @ cov_matrix @ w_mvp
mvp_vol_annual = np.sqrt(port_var)

# ==================== 5. 按要求填充结果字典 ====================
result = {
    'mvp_weights': w_mvp.tolist(),
    'mvp_vol_annual': mvp_vol_annual
}

# 如果需要当堂打印展示，可取消下面一行的注释
# print(result)
