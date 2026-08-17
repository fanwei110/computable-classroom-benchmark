import numpy as np

# 1. 按资产被提及的顺序对应 60/40 权重（A 占 60%）
w = np.array([0.6, 0.4])

# 资产 A 和 B 的年化波动率（小数表示）
vol_A = 0.184
vol_B = 0.297

# 2. 构造相关系数 0.3 与 0.8 两个协方差矩阵
# 协方差 cov(i,j) = rho * vol_i * vol_j
rho_before = 0.3
cov_before = np.array([
    [vol_A**2, rho_before * vol_A * vol_B],
    [rho_before * vol_A * vol_B, vol_B**2]
])

rho_after = 0.8
cov_after = np.array([
    [vol_A**2, rho_after * vol_A * vol_B],
    [rho_after * vol_A * vol_B, vol_B**2]
])

# 3. 计算两个组合波动率，用小数表示
# 组合方差 = w'Σw，组合波动率 = sqrt(w'Σw)
var_before = w.T @ cov_before @ w
vol_before = np.sqrt(var_before)

var_after = w.T @ cov_after @ w
vol_after = np.sqrt(var_after)

# 4. 填充 result
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

# 打印结果以便课堂展示
print(f"相关系数为 0.3 时的组合年化波动率: {result['vol_before_annual']:.4f}")
print(f"相关系数为 0.8 时的组合年化波动率: {result['vol_after_annual']:.4f}")
