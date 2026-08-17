import numpy as np

# 1. 按资产被提及的顺序对应 60/40 权重（A 占 60%）
w_A = 0.6
w_B = 0.4
w = np.array([w_A, w_B])

# 2. 给定资产的年化波动率（小数表示）
sigma_A = 0.184
sigma_B = 0.297

# 协方差计算公式：Cov(A, B) = rho * sigma_A * sigma_B
rho_before = 0.3
rho_after = 0.8

cov_before = rho_before * sigma_A * sigma_B
cov_after = rho_after * sigma_A * sigma_B

# 构造相关系数 0.3 与 0.8 两个协方差矩阵
# 矩阵顺序与权重一致：[A, B]
cov_matrix_before = np.array([
    [sigma_A**2, cov_before],
    [cov_before, sigma_B**2]
])

cov_matrix_after = np.array([
    [sigma_A**2, cov_after],
    [cov_after, sigma_B**2]
])

# 3. 计算两个组合波动率 (组合方差为 w'Σw，波动率为其开方)
var_before = w.T @ cov_matrix_before @ w
vol_before = np.sqrt(var_before)

var_after = w.T @ cov_matrix_after @ w
vol_after = np.sqrt(var_after)

# 4. 填充 result（用小数表示）
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

# 打印结果以便课堂展示
print(f"相关系数为 0.3 时的组合年化波动率: {vol_before:.4%} ({vol_before:.6f})")
print(f"相关系数为 0.8 时的组合年化波动率: {vol_after:.4%} ({vol_after:.6f})")
print(f"波动率变化量: {(vol_after - vol_before):.4%}")
