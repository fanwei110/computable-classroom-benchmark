import numpy as np

# 给定年化波动率（小数形式）
sigma_A = 0.184   # 资产A：18.4%
sigma_B = 0.297   # 资产B：29.7%

# 60/40 组合权重：这里约定 A 占 60%，B 占 40%
w = np.array([0.6, 0.4])

# ---------- 相关系数为 0.3 时的协方差矩阵 ----------
rho_before = 0.3
cov_before = np.array([[sigma_A**2, rho_before * sigma_A * sigma_B],
                       [rho_before * sigma_A * sigma_B, sigma_B**2]])
# 组合方差 = w' Σ w
var_before = w.T @ cov_before @ w
vol_before_annual = np.sqrt(var_before)

# ---------- 相关系数为 0.8 时的协方差矩阵 ----------
rho_after = 0.8
cov_after = np.array([[sigma_A**2, rho_after * sigma_A * sigma_B],
                      [rho_after * sigma_A * sigma_B, sigma_B**2]])
var_after = w.T @ cov_after @ w
vol_after_annual = np.sqrt(var_after)

# 输出要求的字典
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

print(result)
