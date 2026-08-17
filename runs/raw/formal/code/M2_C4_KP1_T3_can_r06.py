import numpy as np

def main():
    # 给定数据 (小数表示)
    sigma_A = 0.184   # 资产 A 年化波动率 18.4%
    sigma_B = 0.297   # 资产 B 年化波动率 29.7%
    rho_before = 0.3  # 相关系数 0.3
    rho_after = 0.8   # 相关系数 0.8

    # 组合权重: A 60%, B 40%
    w = np.array([0.6, 0.4])

    # 构造协方差矩阵的函数
    def cov_matrix(sigma1, sigma2, rho):
        cov = rho * sigma1 * sigma2
        return np.array([[sigma1**2, cov],
                         [cov, sigma2**2]])

    # 计算两个情境下的协方差矩阵
    Sigma_before = cov_matrix(sigma_A, sigma_B, rho_before)
    Sigma_after  = cov_matrix(sigma_A, sigma_B, rho_after)

    # 组合方差 = w' Σ w
    var_before = w @ Sigma_before @ w
    var_after  = w @ Sigma_after @ w

    # 年化波动率
    vol_before_annual = np.sqrt(var_before)
    vol_after_annual  = np.sqrt(var_after)

    # 按照输出契约存入字典
    result = {
        'vol_before_annual': vol_before_annual,
        'vol_after_annual': vol_after_annual
    }

    # 打印结果，方便课堂查看
    print("当相关系数为 0.3 时，60/40 组合的年化波动率: {:.4f} ({:.2f}%)".format(
        vol_before_annual, vol_before_annual * 100))
    print("当相关系数为 0.8 时，60/40 组合的年化波动率: {:.4f} ({:.2f}%)".format(
        vol_after_annual, vol_after_annual * 100))
    print("\n输出字典 result:", result)

    return result

if __name__ == "__main__":
    result = main()
