import numpy as np

def main():
    # 年化波动率
    sigma_A = 0.184  # 资产A
    sigma_B = 0.297  # 资产B

    # 组合权重：60/40，A占60%，B占40%
    w = np.array([0.6, 0.4])

    # 相关系数
    rho_before = 0.3
    rho_after = 0.8

    # 构造协方差矩阵
    def cov_matrix(sigma_A, sigma_B, rho):
        cov = np.array([
            [sigma_A**2, rho * sigma_A * sigma_B],
            [rho * sigma_A * sigma_B, sigma_B**2]
        ])
        return cov

    Sigma_before = cov_matrix(sigma_A, sigma_B, rho_before)
    Sigma_after = cov_matrix(sigma_A, sigma_B, rho_after)

    # 组合方差和波动率
    var_before = w.T @ Sigma_before @ w
    vol_before_annual = np.sqrt(var_before)

    var_after = w.T @ Sigma_after @ w
    vol_after_annual = np.sqrt(var_after)

    # 存储结果
    result = {
        'vol_before_annual': vol_before_annual,
        'vol_after_annual': vol_after_annual
    }

    # 打印结果（保留四位小数以便课堂展示）
    print(f"组合波动率（相关系数=0.3）: {vol_before_annual:.4f} ({vol_before_annual*100:.2f}%)")
    print(f"组合波动率（相关系数=0.8）: {vol_after_annual:.4f} ({vol_after_annual*100:.2f}%)")
    print(f"变化: {vol_after_annual - vol_before_annual:.4f}")

    return result

if __name__ == "__main__":
    result = main()
