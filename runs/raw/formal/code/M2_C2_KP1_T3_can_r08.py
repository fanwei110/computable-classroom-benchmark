import numpy as np

def main():
    # 给定年化波动率
    sigma_A = 0.184   # 18.4%
    sigma_B = 0.297   # 29.7%

    # 60/40 组合：假设资产A占60%，资产B占40%
    w = np.array([0.6, 0.4])

    # 相关系数
    rho_before = 0.3
    rho_after  = 0.8

    # 构造协方差矩阵
    cov_before = np.array([
        [sigma_A**2,                     rho_before * sigma_A * sigma_B],
        [rho_before * sigma_A * sigma_B, sigma_B**2]
    ])
    cov_after = np.array([
        [sigma_A**2,                    rho_after * sigma_A * sigma_B],
        [rho_after * sigma_A * sigma_B, sigma_B**2]
    ])

    # 组合年化波动率 (标准差)
    vol_before = np.sqrt(w @ cov_before @ w)
    vol_after  = np.sqrt(w @ cov_after @ w)

    # 输出合约
    result = {
        'vol_before_annual': vol_before,
        'vol_after_annual': vol_after
    }

    print(result)

if __name__ == '__main__':
    main()
