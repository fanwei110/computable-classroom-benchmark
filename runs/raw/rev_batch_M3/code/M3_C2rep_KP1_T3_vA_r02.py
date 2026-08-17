import numpy as np

# ================= 1. 确定权重与资产参数 =================
# 假设：按照惯例，60/40 组合对应 资产A权重为60%，资产B权重为40%
w_A = 0.6
w_B = 0.4
weights = np.array([w_A, w_B])

# 资产年化波动率
vol_A = 0.184
vol_B = 0.297

# ================= 2. 构造协方差矩阵 =================
# 相关系数设定
rho_before = 0.3
rho_after = 0.8

# 计算协方差 cov(A,B) = rho * vol_A * vol_B
cov_AB_before = rho_before * vol_A * vol_B
cov_AB_after = rho_after * vol_A * vol_B

# 构造协方差矩阵 Σ
# Σ = [[vol_A^2, cov_AB], [cov_AB, vol_B^2]]
cov_matrix_before = np.array([
    [vol_A**2, cov_AB_before],
    [cov_AB_before, vol_B**2]
])

cov_matrix_after = np.array([
    [vol_A**2, cov_AB_after],
    [cov_AB_after, vol_B**2]
])

# ================= 3. 计算组合波动率 =================
# 组合方差公式：σ_p^2 = w'Σw
var_before = weights.T @ cov_matrix_before @ weights
var_after = weights.T @ cov_matrix_after @ weights

# 组合年化波动率
vol_before_annual = np.sqrt(var_before)
vol_after_annual = np.sqrt(var_after)

# ================= 4. 填充 result =================
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# 打印结果以供课堂展示
print(f"相关系数为 0.3 时，60/40组合的年化波动率: {vol_before_annual:.4f} ({vol_before_annual*100:.2f}%)")
print(f"相关系数为 0.8 时，60/40组合的年化波动率: {vol_after_annual:.4f} ({vol_after_annual*100:.2f}%)")
print(f"波动率变化量: {(vol_after_annual - vol_before_annual)*100:.2f}%")
