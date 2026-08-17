import numpy as np

# 1. 按资产被提及的顺序对应 60/40 权重（A 占 60%，B 占 40%）
w = np.array([0.6, 0.4])

# 资产的年化波动率（小数表示）
sigma_A = 0.184
sigma_B = 0.297

# 2. 构造相关系数 0.3 与 0.8 两个协方差矩阵
# 协方差公式: Cov(A, B) = rho * sigma_A * sigma_B
cov_before = np.array([
    [sigma_A**2, 0.3 * sigma_A * sigma_B],
    [0.3 * sigma_A * sigma_B, sigma_B**2]
])

cov_after = np.array([
    [sigma_A**2, 0.8 * sigma_A * sigma_B],
    [0.8 * sigma_A * sigma_B, sigma_B**2]
])

# 3. 计算两个组合方差与波动率，用小数表示
# 组合方差公式: w'Σw
var_before = w.T @ cov_before @ w
var_after = w.T @ cov_after @ w

vol_before_annual = np.sqrt(var_before)
vol_after_annual = np.sqrt(var_after)

# 4. 填充 result
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# (可选) 课堂投屏展示验证
print(f"相关系数 0.3 时的组合年化波动率: {vol_before_annual:.4f} (即 {vol_before_annual*100:.2f}%)")
print(f"相关系数 0.8 时的组合年化波动率: {vol_after_annual:.4f} (即 {vol_after_annual*100:.2f}%)")
print(f"波动率变化: 相关系数升高导致组合波动率增加 {vol_after_annual - vol_before_annual:.4f}")
