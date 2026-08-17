import numpy as np

# 资产年化波动率
sigma_A = 0.184  # 18.4%
sigma_B = 0.297  # 29.7%

# 组合权重：资产 A 占 60%，资产 B 占 40%
w = np.array([0.6, 0.4])

# 相关系数
rho_before = 0.3
rho_after  = 0.8

def cov_matrix(s1, s2, rho):
    """返回由年化波动率 s1, s2 和相关系数 rho 构造的协方差矩阵"""
    cov = rho * s1 * s2
    return np.array([[s1**2, cov],
                     [cov,    s2**2]])

# 构造协方差矩阵
Sigma_before = cov_matrix(sigma_A, sigma_B, rho_before)
Sigma_after  = cov_matrix(sigma_A, sigma_B, rho_after)

# 组合年化波动率
vol_before = np.sqrt(w @ Sigma_before @ w)
vol_after  = np.sqrt(w @ Sigma_after @ w)

# 按要求存入字典
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual':  vol_after
}

if __name__ == "__main__":
    print(result)
