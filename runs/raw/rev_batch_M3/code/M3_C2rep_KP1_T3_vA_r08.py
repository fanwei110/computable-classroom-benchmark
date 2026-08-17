import numpy as np

# ==================== 1. 确定权重与参数 ====================
# 按照惯例，"60/40组合"指代先提及的资产A权重为60%，后提及的资产B权重为40%
w_A = 0.6
w_B = 0.4
w = np.array([w_A, w_B])

# 资产年化波动率（标准差）
vol_A = 0.184
vol_B = 0.297

# 相关系数设定
rho_before = 0.3
rho_after = 0.8

# ==================== 2. 构造协方差矩阵 ====================
# 协方差 cov_AB = rho_AB * vol_A * vol_B
def build_cov_matrix(rho, vol_a, vol_b):
    cov_ab = rho * vol_a * vol_b
    # 协方差矩阵 Sigma = [[var_a, cov_ab], [cov_ab, var_b]]
    cov_matrix = np.array([
        [vol_a**2, cov_ab],
        [cov_ab, vol_b**2]
    ])
    return cov_matrix

cov_before = build_cov_matrix(rho_before, vol_A, vol_B)
cov_after  = build_cov_matrix(rho_after, vol_A, vol_B)

# ==================== 3. 计算组合波动率 ====================
# 组合方差公式: sigma_p^2 = w' * Sigma * w
# 组合波动率: sigma_p = sqrt(w' * Sigma * w)
def calc_portfolio_vol(weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)

vol_before_annual = calc_portfolio_vol(w, cov_before)
vol_after_annual  = calc_portfolio_vol(w, cov_after)

# ==================== 4. 填充 result ====================
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# 输出结果以便教师投屏展示
print(f"相关系数为 0.3 时的 60/40 组合年化波动率: {vol_before_annual:.4%}")
print(f"相关系数为 0.8 时的 60/40 组合年化波动率: {vol_after_annual:.4%}")
print(f"波动率变化量: {(vol_after_annual - vol_before_annual):.4%}")
print("result =", result)
