import numpy as np

# 1. 按资产被提及的顺序对应 60/40 权重（A 占 60%，B 占 40%）
w = np.array([0.6, 0.4])

# 资产年化波动率（小数表示）
sigma_A = 0.184
sigma_B = 0.297

# 2. 构造相关系数 0.3 与 0.8 两个协方差矩阵
# 协方差公式：Cov(A, B) = rho * sigma_A * sigma_B
rho_before = 0.3
rho_after = 0.8

cov_before = rho_before * sigma_A * sigma_B
Sigma_before = np.array([
    [sigma_A**2, cov_before],
    [cov_before, sigma_B**2]
])

cov_after = rho_after * sigma_A * sigma_B
Sigma_after = np.array([
    [sigma_A**2, cov_after],
    [cov_after, sigma_B**2]
])

# 3. 计算两个组合波动率，用小数表示
# 组合方差公式：w'Σw
var_before = w.T @ Sigma_before @ w
var_after = w.T @ Sigma_after @ w

vol_before = np.sqrt(var_before)
vol_after = np.sqrt(var_after)

# 4. 填充 result
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

# 为了课堂投屏展示效果，打印结果
print(f"相关系数为 0.3 时的组合波动率: {result['vol_before_annual']:.4%}")
print(f"相关系数为 0.8 时的组合波动率: {result['vol_after_annual']:.4%}")
print(f"result = {result}")
