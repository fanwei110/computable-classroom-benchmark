import numpy as np

# 1. 按资产被提及的顺序对应 60/40 权重（A 占 60%，B 占 40%）
w = np.array([0.6, 0.4])

# 资产年化波动率（小数表示）
vol_A = 0.184
vol_B = 0.297

# 2. 构造相关系数 0.3 与 0.8 两个协方差矩阵
# 协方差公式：Cov(A, B) = rho * vol_A * vol_B
cov_AB_03 = 0.3 * vol_A * vol_B
cov_AB_08 = 0.8 * vol_A * vol_B

cov_matrix_before = np.array([
    [vol_A**2, cov_AB_03],
    [cov_AB_03, vol_B**2]
])

cov_matrix_after = np.array([
    [vol_A**2, cov_AB_08],
    [cov_AB_08, vol_B**2]
])

# 3. 计算两个组合波动率，用小数表示
# 组合方差公式：sigma_p^2 = w' * Sigma * w
var_before = w.T @ cov_matrix_before @ w
var_after = w.T @ cov_matrix_after @ w

vol_before = np.sqrt(var_before)
vol_after = np.sqrt(var_after)

# 4. 填充 result
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

# 课堂投屏辅助打印（非必须，但有助于展示计算过程与结果）
print(f"相关系数为 0.3 时的组合方差: {var_before:.6f}")
print(f"相关系数为 0.3 时的组合年化波动率: {vol_before:.4%}")
print("-" * 30)
print(f"相关系数为 0.8 时的组合方差: {var_after:.6f}")
print(f"相关系数为 0.8 时的组合年化波动率: {vol_after:.4%}")
print("-" * 30)
print("result 字典内容:", result)
