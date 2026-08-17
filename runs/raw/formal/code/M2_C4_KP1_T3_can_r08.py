import numpy as np

def main():
    # 给定参数：年化波动率（小数）
    sigma_A = 0.184
    sigma_B = 0.297

    # 组合权重：A 占 60%，B 占 40%
    w = np.array([0.6, 0.4])

    # 相关系数
    rho_before = 0.3
    rho_after = 0.8

    # 构造协方差矩阵的函数
    def cov_matrix(rho):
        cov_AB = rho * sigma_A * sigma_B
        return np.array([[sigma_A**2, cov_AB],
                         [cov_AB, sigma_B**2]])

    cov_before = cov_matrix(rho_before)
    cov_after = cov_matrix(rho_after)

    # 计算组合方差与波动率
    var_before = w @ cov_before @ w
    var_after = w @ cov_after @ w

    vol_before = np.sqrt(var_before)
    vol_after = np.sqrt(var_after)

    # 输出契约
    result = {
        'vol_before_annual': vol_before,
        'vol_after_annual': vol_after
    }

    print(result)

if __name__ == "__main__":
    main()
