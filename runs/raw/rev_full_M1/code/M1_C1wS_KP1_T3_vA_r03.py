import numpy as np

# 1. 确定权重与资产对应关系
# 假设 A 占 60%，B 占 40%
weights = np.array([0.6, 0.4])  # [A, B]

# 2. 资产波动率（年化，已给出）
vol_A = 0.184
vol_B = 0.297

# 3. 构造协方差矩阵
# 相关系数 0.3 时的协方差矩阵
corr_before = 0.3
cov_before = np.array([
    [vol_A ** 2, corr_before * vol_A * vol_B],
    [corr_before * vol_A * vol_B, vol_B ** 2]
])

# 相关系数 0.8 时的协方差矩阵
corr_after = 0.8
cov_after = np.array([
    [vol_A ** 2, corr_after * vol_A * vol_B],
    [corr_after * vol_A * vol_B, vol_B ** 2]
])

# 4. 计算组合波动率（年化）
portfolio_vol_before = np.sqrt(weights.T @ cov_before @ weights)
portfolio_vol_after = np.sqrt(weights.T @ cov_after @ weights)

# 5. 填充 result 字典
result = {
    'vol_before_annual': portfolio_vol_before,
    'vol_after_annual': portfolio_vol_after
}

print(result)
