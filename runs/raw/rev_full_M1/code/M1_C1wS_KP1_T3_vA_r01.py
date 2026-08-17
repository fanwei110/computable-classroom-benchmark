import numpy as np

# 1. 确定权重与资产对应关系：A占60%，B占40%
weights = np.array([0.6, 0.4])  # [A, B]

# 2. 资产波动率（年化）
vol_A = 0.184
vol_B = 0.297

# 3. 构造协方差矩阵
# 相关系数0.3的协方差矩阵
corr_before = 0.3
cov_before = np.array([
    [vol_A ** 2, corr_before * vol_A * vol_B],
    [corr_before * vol_A * vol_B, vol_B ** 2]
])

# 相关系数0.8的协方差矩阵
corr_after = 0.8
cov_after = np.array([
    [vol_A ** 2, corr_after * vol_A * vol_B],
    [corr_after * vol_A * vol_B, vol_B ** 2]
])

# 4. 计算组合波动率（年化）
# 组合方差 = w'Σw
portfolio_var_before = weights.T @ cov_before @ weights
portfolio_vol_before = np.sqrt(portfolio_var_before)

portfolio_var_after = weights.T @ cov_after @ weights
portfolio_vol_after = np.sqrt(portfolio_var_after)

# 5. 填充结果字典
result = {
    'vol_before_annual': round(portfolio_vol_before, 6),  # 保留6位小数
    'vol_after_annual': round(portfolio_vol_after, 6)
}

print(result)
