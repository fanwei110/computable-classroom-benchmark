import numpy as np

def main():
    # 给定参数
    sigma_A = 0.184   # 资产 A 年化波动率
    sigma_B = 0.297   # 资产 B 年化波动率
    w = np.array([0.6, 0.4])  # A 占 60%，B 占 40%

    # 相关系数
    rho_before = 0.3
    rho_after  = 0.8

    # 协方差矩阵函数
    def cov_matrix(sigma1, sigma2, rho):
        cov = rho * sigma1 * sigma2
        return np.array([
            [sigma1**2, cov],
            [cov,       sigma2**2]
        ])

    # 计算变化前的协方差与组合波动率
    Sigma_before = cov_matrix(sigma_A, sigma_B, rho_before)
    var_before = w @ Sigma_before @ w
    vol_before = np.sqrt(var_before)  # 年化波动率，小数

    # 计算变化后的协方差与组合波动率
    Sigma_after = cov_matrix(sigma_A, sigma_B, rho_after)
    var_after = w @ Sigma_after @ w
    vol_after = np.sqrt(var_after)

    # 结果存入字典
    result = {
        'vol_before_annual': vol_before,
        'vol_after_annual': vol_after
    }

    # 打印结果以便查看
    print("资产 A 与 B 的 60/40 组合年化波动率：")
    print(f"相关系数为 0.3 时：{vol_before:.4f} ({vol_before*100:.2f}%)")
    print(f"相关系数为 0.8 时：{vol_after:.4f} ({vol_after*100:.2f}%)")
    print("\nresult =", result)

    return result

if __name__ == "__main__":
    result = main()
