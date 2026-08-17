import numpy as np

# ======================================================
# 马科维茨均值-方差：60/40 组合波动率对相关系数的敏感性
# ======================================================

# 题目给定（年化）
sigma_A = 0.184   # 资产 A 的年化波动率
sigma_B = 0.297   # 资产 B 的年化波动率

# 权重设定：60/40 指 A 占 60%，B 占 40%
w = np.array([0.6, 0.4])

# 两个情景的相关系数
rho_before = 0.3
rho_after  = 0.8

def portfolio_vol(sigma_A, sigma_B, rho, w):
    """
    计算给定相关系数下两资产组合的年化波动率。
    组合方差 = w' Σ w，Σ_ij = σ_i * σ_j * ρ_ij
    """
    # 构建协方差矩阵
    cov_matrix = np.array([
        [sigma_A**2,               rho * sigma_A * sigma_B],
        [rho * sigma_A * sigma_B,  sigma_B**2]
    ])
    # 组合方差
    port_variance = w @ cov_matrix @ w  # 等于 w.T @ cov @ w
    return np.sqrt(port_variance)

# 计算变化前后的年化波动率
vol_before = portfolio_vol(sigma_A, sigma_B, rho_before, w)
vol_after  = portfolio_vol(sigma_A, sigma_B, rho_after,  w)

# 输出结果字典
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

# 投屏展示：打印清晰的结果
print("===== 60/40 组合波动率对相关系数变动的响应 =====")
print(f"资产 A 年化波动率: {sigma_A:.1%}")
print(f"资产 B 年化波动率: {sigma_B:.1%}")
print(f"组合权重 (A/B): {w[0]:.0%}/{w[1]:.0%}")
print("-" * 45)
print(f"相关系数 ρ = {rho_before} 时，组合年化波动率: {vol_before:.4%}")
print(f"相关系数 ρ = {rho_after} 时，组合年化波动率: {vol_after:.4%}")
print(f"波动率变动: {vol_after - vol_before:+.4%}")
print("-" * 45)
print("结果字典 (result):")
print(result)
