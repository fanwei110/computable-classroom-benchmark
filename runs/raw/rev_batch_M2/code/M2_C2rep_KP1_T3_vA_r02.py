import numpy as np

def main():
    # 给定年化波动率
    sigma_A = 0.184   # 资产 A 年化波动率 18.4%
    sigma_B = 0.297   # 资产 B 年化波动率 29.7%

    # 组合权重：60% A, 40% B
    w = np.array([0.6, 0.4])

    # 两个相关系数情景
    rho_before = 0.3
    rho_after  = 0.8

    # 协方差矩阵构造函数
    def build_cov(s1, s2, rho):
        cov = rho * s1 * s2
        return np.array([[s1**2, cov],
                         [cov,    s2**2]])

    # 情景1：相关系数 = 0.3
    cov_before = build_cov(sigma_A, sigma_B, rho_before)
    var_before = w @ cov_before @ w
    vol_before_annual = np.sqrt(var_before)

    # 情景2：相关系数 = 0.8
    cov_after = build_cov(sigma_A, sigma_B, rho_after)
    var_after = w @ cov_after @ w
    vol_after_annual = np.sqrt(var_after)

    # 输出契约
    result = {
        'vol_before_annual': vol_before_annual,
        'vol_after_annual': vol_after_annual
    }

    print("Result dictionary:")
    print(result)

if __name__ == "__main__":
    main()
