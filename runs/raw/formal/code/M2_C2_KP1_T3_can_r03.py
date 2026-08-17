import numpy as np

def main():
    # 年化波动率
    sigma_A = 0.184   # 资产A的年化波动率
    sigma_B = 0.297   # 资产B的年化波动率

    # 组合权重 (60/40)
    w = np.array([0.6, 0.4])  # [A的比重, B的比重]

    # 两种相关系数
    rho_before = 0.3
    rho_after  = 0.8

    def cov_matrix(rho):
        """根据相关系数构造协方差矩阵"""
        cov_AB = rho * sigma_A * sigma_B
        return np.array([[sigma_A**2, cov_AB],
                         [cov_AB,    sigma_B**2]])

    cov_before = cov_matrix(rho_before)
    cov_after  = cov_matrix(rho_after)

    # 组合方差 w^T Σ w
    var_before = w @ cov_before @ w
    var_after  = w @ cov_after  @ w

    # 年化组合波动率
    vol_before_annual = np.sqrt(var_before)
    vol_after_annual  = np.sqrt(var_after)

    # 按要求存入结果字典
    result = {
        'vol_before_annual': vol_before_annual,
        'vol_after_annual':  vol_after_annual
    }

    # 输出结果，可直接被教师查看
    print(result)
    return result

if __name__ == "__main__":
    main()
