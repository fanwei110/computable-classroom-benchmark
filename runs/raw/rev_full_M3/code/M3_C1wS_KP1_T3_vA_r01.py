import numpy as np

# ================= 1. 参数设定与权重确定 =================
# 假设：A占六成，B占四成，即 w_A = 0.6, w_B = 0.4
w_A = 0.6
w_B = 0.4
weights = np.array([w_A, w_B])

# 资产波动率（年化）
vol_A = 0.184
vol_B = 0.297

# 相关系数变化前后的值
rho_before = 0.3
rho_after = 0.8

# ================= 2. 构造协方差矩阵 =================
# 资产方差
var_A = vol_A ** 2
var_B = vol_B ** 2

# 协方差：cov(A, B) = rho * vol_A * vol_B
cov_AB_before = rho_before * vol_A * vol_B
cov_AB_after = rho_after * vol_A * vol_B

# 构造协方差矩阵 Sigma
cov_matrix_before = np.array([
    [var_A, cov_AB_before],
    [cov_AB_before, var_B]
])

cov_matrix_after = np.array([
    [var_A, cov_AB_after],
    [cov_AB_after, var_B]
])

# ================= 3. 计算组合波动率 =================
# 组合方差公式：sigma_p^2 = w' * Sigma * w
var_port_before = weights.T @ cov_matrix_before @ weights
var_port_after = weights.T @ cov_matrix_after @ weights

# 组合波动率（年化） = sqrt(组合方差)
vol_port_before = np.sqrt(var_port_before)
vol_port_after = np.sqrt(var_port_after)

# ================= 4. 填充结果 =================
result = {
    'vol_before_annual': vol_port_before,
    'vol_after_annual': vol_port_after
}

# 课堂投屏展示辅助打印
print(f"相关系数为 {rho_before} 时，组合年化波动率: {vol_port_before:.4%}")
print(f"相关系数为 {rho_after} 时，组合年化波动率: {vol_port_after:.4%}")
