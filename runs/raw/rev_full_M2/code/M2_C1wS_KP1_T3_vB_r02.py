import numpy as np

# 资产参数
sigma_A = 0.184   # 资产A年化波动率
sigma_B = 0.297   # 资产B年化波动率
w = np.array([0.6, 0.4])   # 60/40 权重

# 不同相关系数
rho_before = 0.3
rho_after = 0.8

def cov_matrix(s1, s2, rho):
    """构造两只资产的协方差矩阵"""
    cov = rho * s1 * s2
    return np.array([[s1**2, cov],
                     [cov, s2**2]])

# 构造协方差矩阵
cov_before = cov_matrix(sigma_A, sigma_B, rho_before)
cov_after = cov_matrix(sigma_A, sigma_B, rho_after)

# 计算组合方差
var_before = w @ cov_before @ w
var_after = w @ cov_after @ w

# 组合年化波动率
vol_before = np.sqrt(var_before)
vol_after = np.sqrt(var_after)

# 按输出契约构建结果字典
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

print(result)
