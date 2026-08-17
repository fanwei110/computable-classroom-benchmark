import numpy as np

# ==========================================
# 1. 确定权重与基本参数
# ==========================================
# 约定：60/40组合表示资产A权重为60%，资产B权重为40%
w = np.array([0.6, 0.4])

# 题目给定的年化波动率
vol_A = 0.184
vol_B = 0.297

# 计算资产方差
var_A = vol_A ** 2
var_B = vol_B ** 2

# ==========================================
# 2. 构造相关系数 0.3 与 0.8 两个协方差矩阵
# ==========================================
rho_before = 0.3
rho_after = 0.8

# 协方差 = 相关系数 * 资产A标准差 * 资产B标准差
cov_before = rho_before * vol_A * vol_B
cov_after = rho_after * vol_A * vol_B

# 协方差矩阵
cov_matrix_before = np.array([
    [var_A, cov_before],
    [cov_before, var_B]
])

cov_matrix_after = np.array([
    [var_A, cov_after],
    [cov_after, var_B]
])

# ==========================================
# 3. 计算两个组合波动率
# ==========================================
# 马科维茨组合方差公式：sigma_p^2 = w' * Sigma * w
var_portfolio_before = w @ cov_matrix_before @ w
var_portfolio_after = w @ cov_matrix_after @ w

# 组合波动率 = sqrt(组合方差)
# 由于输入波动率已是年化，计算所得亦为年化波动率
vol_before_annual = np.sqrt(var_portfolio_before)
vol_after_annual = np.sqrt(var_portfolio_after)

# ==========================================
# 4. 填充 result
# ==========================================
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# 课堂投屏辅助打印（方便教师讲解验证）
print(f"资产A权重: {w[0]:.0%}, 资产B权重: {w[1]:.0%}")
print(f"相关系数为 {rho_before} 时的组合年化波动率: {vol_before_annual:.4%}")
print(f"相关系数为 {rho_after} 时的组合年化波动率: {vol_after_annual:.4%}")
print(f"波动率变化: 升高了 {(vol_after_annual - vol_before_annual):.4%}")
