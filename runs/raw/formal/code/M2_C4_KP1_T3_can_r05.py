import numpy as np

def main():
    # 给定的年化波动率（小数）
    sigma_A = 0.184
    sigma_B = 0.297

    # 权重：A占60%，B占40%
    w = np.array([0.6, 0.4])

    # 情况1：相关系数 0.3
    rho1 = 0.3
    cov_AB1 = rho1 * sigma_A * sigma_B
    cov_matrix1 = np.array([
        [sigma_A**2, cov_AB1],
        [cov_AB1, sigma_B**2]
    ])
    # 组合方差与波动率
    var1 = w @ cov_matrix1 @ w  # w' Σ w
    vol1 = np.sqrt(var1)

    # 情况2：相关系数 0.8
    rho2 = 0.8
    cov_AB2 = rho2 * sigma_A * sigma_B
    cov_matrix2 = np.array([
        [sigma_A**2, cov_AB2],
        [cov_AB2, sigma_B**2]
    ])
    var2 = w @ cov_matrix2 @ w
    vol2 = np.sqrt(var2)

    # 存放结果
    result = {
        'vol_before_annual': vol1,   # 相关系数 0.3 时的年化组合波动率
        'vol_after_annual': vol2    # 相关系数 0.8 时的年化组合波动率
    }

    return result

if __name__ == "__main__":
    result = main()
    print(result)
