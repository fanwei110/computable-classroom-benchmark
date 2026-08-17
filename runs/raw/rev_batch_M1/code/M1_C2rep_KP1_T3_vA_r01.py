import numpy as np

# 1. 确定权重对应方式：w_A = 0.6, w_B = 0.4
weights = np.array([0.6, 0.4])

# 资产年化波动率（标准差）
vol_A_annual = 0.184
vol_B_annual = 0.297

# 2. 构造协方差矩阵
# 相关系数 ρ = 0.3
rho_before = 0.3
cov_before = rho_before * vol_A_annual * vol_B_annual
Sigma_before = np.array([
    [vol_A_annual**2, cov_before],
    [cov_before, vol_B_annual**2]
])

# 相关系数 ρ = 0.8
rho_after = 0.8
cov_after = rho_after * vol_A_annual * vol_B_annual
Sigma_after = np.array([
    [vol_A_annual**2, cov_after],
    [cov_after, vol_B_annual**2]
])

# 3. 计算组合波动率（年化）
portfolio_vol_before = np.sqrt(weights.T @ Sigma_before @ weights)
portfolio_vol_after = np.sqrt(weights.T @ Sigma_after @ weights)

# 4. 填充 result 字典
result = {
    'vol_before_annual': portfolio_vol_before,
    'vol_after_annual': portfolio_vol_after
}
