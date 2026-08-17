import numpy as np

# 资产年化波动率（近似值）
sigma_A = 0.184  # 大约 18.4%
sigma_B = 0.297  # 大约 29.7%

# 组合权重：A 占 60%，B 占 40%
w = np.array([0.6, 0.4])

# 相关系数
rho_before = 0.3
rho_after = 0.8

# 计算协方差矩阵
def cov_matrix(sigma_A, sigma_B, rho):
    cov_ab = rho * sigma_A * sigma_B
    return np.array([[sigma_A**2, cov_ab],
                     [cov_ab, sigma_B**2]])

cov_before = cov_matrix(sigma_A, sigma_B, rho_before)
cov_after  = cov_matrix(sigma_A, sigma_B, rho_after)

# 组合方差 = w' Σ w
var_before = w @ cov_before @ w
var_after  = w @ cov_after @ w

# 组合波动率（年化标准差）
vol_before = np.sqrt(var_before)
vol_after  = np.sqrt(var_after)

# 输出契约：存放到名为 result 的字典
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

# 便于演示，打印结果
print(f"组合波动率（rho=0.3）: {vol_before:.4f} ({vol_before*100:.2f}%)")
print(f"组合波动率（rho=0.8）: {vol_after:.4f} ({vol_after*100:.2f}%)")
print("结果字典:", result)
