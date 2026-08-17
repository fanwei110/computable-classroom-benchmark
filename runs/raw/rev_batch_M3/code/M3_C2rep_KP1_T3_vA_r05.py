import numpy as np

# ==================== 1. 确定参数与权重 ====================
# 根据题意"A和B的60/40组合"，按常规顺序设定资产A权重为60%，资产B权重为40%
vol_A = 0.184
vol_B = 0.297
weights = np.array([0.6, 0.4])

# ==================== 2. 构造协方差矩阵 ====================
# 协方差矩阵公式: Sigma = [[vol_A^2, rho*vol_A*vol_B], [rho*vol_A*vol_B, vol_B^2]]
def build_cov_matrix(vol_A, vol_B, rho):
    cov_AB = rho * vol_A * vol_B
    return np.array([
        [vol_A**2, cov_AB],
        [cov_AB,   vol_B**2]
    ])

cov_matrix_before = build_cov_matrix(vol_A, vol_B, rho=0.3)
cov_matrix_after  = build_cov_matrix(vol_A, vol_B, rho=0.8)

# ==================== 3. 计算组合波动率 ====================
# 马科维茨组合方差公式: sigma_p^2 = w' Sigma w
def calc_portfolio_vol(w, cov_matrix):
    port_var = w.T @ cov_matrix @ w
    return np.sqrt(port_var)

vol_before = calc_portfolio_vol(weights, cov_matrix_before)
vol_after  = calc_portfolio_vol(weights, cov_matrix_after)

# ==================== 4. 填充 result ====================
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

# 课堂投屏辅助打印（便于教师展示逻辑与结果）
print(f"相关系数为 0.3 时的协方差矩阵:\n{cov_matrix_before}\n")
print(f"相关系数为 0.8 时的协方差矩阵:\n{cov_matrix_after}\n")
print(f"60/40 组合波动率 (rho=0.3): {vol_before:.4%}")
print(f"60/40 组合波动率 (rho=0.8): {vol_after:.4%}")
print(f"\n最终结果字典 result: {result}")
