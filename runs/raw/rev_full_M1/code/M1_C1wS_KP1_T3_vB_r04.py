import numpy as np

# 1. 确定权重对应方式：60% 给 A，40% 给 B
weights = np.array([0.6, 0.4])

# 资产波动率（年化）
vol_A = 0.184
vol_B = 0.297

# 2. 构造协方差矩阵
# 相关系数 0.3
corr_before = 0.3
cov_before = corr_before * vol_A * vol_B
Sigma_before = np.array([
    [vol_A**2, cov_before],
    [cov_before, vol_B**2]
])

# 相关系数 0.8
corr_after = 0.8
cov_after = corr_after * vol_A * vol_B
Sigma_after = np.array([
    [vol_A**2, cov_after],
    [cov_after, vol_B**2]
])

# 3. 计算组合波动率（年化）
# 组合方差 = w'Σw
portfolio_var_before = weights.T @ Sigma_before @ weights
portfolio_vol_before = np.sqrt(portfolio_var_before)

portfolio_var_after = weights.T @ Sigma_after @ weights
portfolio_vol_after = np.sqrt(portfolio_var_after)

# 4. 填充 result 字典
result = {
    'vol_before_annual': portfolio_vol_before,
    'vol_after_annual': portfolio_vol_after
}

# 输出结果（供验证）
print(result)
