import numpy as np

# 设置随机种子以保证可复现性
np.random.seed(42)

# 定义资产年化波动率
vol1 = 0.187
vol2 = 0.243
vol3 = 0.312

# 定义相关系数矩阵
rho12 = 0.21
rho13 = -0.13
rho23 = 0.37

# 构建协方差矩阵
sigma = np.array([
    [vol1**2,                 vol1 * vol2 * rho12, vol1 * vol3 * rho13],
    [vol1 * vol2 * rho12,     vol2**2,             vol2 * vol3 * rho23],
    [vol1 * vol3 * rho13,     vol2 * vol3 * rho23, vol3**2]
])

# 资产数量
n = 3

# 全局最小方差组合权重 (允许卖空，资金全部投出)
# 权重公式: w = (Σ^{-1} * 1) / (1^T * Σ^{-1} * 1)
ones = np.ones(n)
sigma_inv = np.linalg.inv(sigma)
mvp_weights = sigma_inv @ ones / (ones @ sigma_inv @ ones)

# 计算组合年化波动率
mvp_variance = mvp_weights @ sigma @ mvp_weights
mvp_vol_annual = np.sqrt(mvp_variance)

# 输出结果字典
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 打印结果以便检查
print("全局最小方差组合权重 (资产1, 资产2, 资产3):")
print(mvp_weights)
print(f"\n组合年化波动率: {mvp_vol_annual:.4f} ({mvp_vol_annual*100:.2f}%)")
