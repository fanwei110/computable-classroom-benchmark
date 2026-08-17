import numpy as np

# ==========================================
# 《证券投资学》课堂演示：马科维茨组合波动率计算
# ==========================================

# 步骤1：自行确定 60/40 权重与两只资产的对应方式
# 假设：常规表述中 "A 和 B 的 60/40 组合" 指 A 占 60%，B 占 40%
w_A = 0.6
w_B = 0.4
weights = np.array([w_A, w_B])

# 资产年化波动率
sigma_A = 0.184
sigma_B = 0.297
sigmas = np.array([sigma_A, sigma_B])

# 步骤2：构造相关系数 0.3 与 0.8 两个协方差矩阵
# 协方差矩阵公式：Σ = diag(σ) @ C @ diag(σ)，其中C为相关系数矩阵
def get_covariance_matrix(rho, sigmas):
    corr_matrix = np.array([[1.0, rho],
                            [rho, 1.0]])
    # 使用对角矩阵乘法计算协方差矩阵
    cov_matrix = np.diag(sigmas) @ corr_matrix @ np.diag(sigmas)
    return cov_matrix

cov_before = get_covariance_matrix(rho=0.3, sigmas=sigmas)
cov_after  = get_covariance_matrix(rho=0.8, sigmas=sigmas)

# 步骤3：计算两个组合波动率
# 组合方差公式：σ_p^2 = w'Σw
var_before = weights.T @ cov_before @ weights
var_after  = weights.T @ cov_after @ weights

vol_before_annual = np.sqrt(var_before)
vol_after_annual  = np.sqrt(var_after)

# 步骤4：填充 result
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# 以下为课堂投屏展示辅助打印，不影响输出契约
print("=== 马科维茨均值-方差组合理论：相关系数变动对组合波动率的影响 ===")
print(f"资产 A 年化波动率: {sigma_A:.1%}")
print(f"资产 B 年化波动率: {sigma_B:.1%}")
print(f"组合权重: A={w_A:.0%}, B={w_B:.0%}")
print("-" * 50)
print(f"当相关系数 = 0.3 时，协方差矩阵:\n{cov_before}")
print(f"组合年化波动率: {vol_before_annual:.4%}")
print("-" * 50)
print(f"当相关系数 = 0.8 时，协方差矩阵:\n{cov_after}")
print(f"组合年化波动率: {vol_after_annual:.4%}")
print("-" * 50)
print(f"相关系数从 0.3 升至 0.8，组合波动率增加了: {(vol_after_annual - vol_before_annual):.4%}")
print(f"\n要求的输出结果 result 字典:\n{result}")
