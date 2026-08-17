import numpy as np

# 1. 确定权重对应方式：60/40 组合，A 占 60%，B 占 40%
weights = np.array([0.6, 0.4])  # [A, B]

# 给定年化波动率（标准差）
vol_A_annual = 0.184
vol_B_annual = 0.297

# 2. 构造协方差矩阵
# 相关系数 ρ = 0.3
rho_before = 0.3
cov_before = np.array([
    [vol_A_annual ** 2, rho_before * vol_A_annual * vol_B_annual],
    [rho_before * vol_A_annual * vol_B_annual, vol_B_annual ** 2]
])

# 相关系数 ρ = 0.8
rho_after = 0.8
cov_after = np.array([
    [vol_A_annual ** 2, rho_after * vol_A_annual * vol_B_annual],
    [rho_after * vol_A_annual * vol_B_annual, vol_B_annual ** 2]
])

# 3. 计算组合波动率（年化）
# 组合方差 = w'Σw
portfolio_var_before = weights.T @ cov_before @ weights
portfolio_vol_before_annual = np.sqrt(portfolio_var_before)

portfolio_var_after = weights.T @ cov_after @ weights
portfolio_vol_after_annual = np.sqrt(portfolio_var_after)

# 4. 填充 result 字典
result = {
    'vol_before_annual': portfolio_vol_before_annual,
    'vol_after_annual': portfolio_vol_after_annual
}
