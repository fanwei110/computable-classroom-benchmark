import numpy as np

def main():
    # 给定数据
    sigma_A = 0.184   # A的波动率（年化）
    sigma_B = 0.297   # B的波动率（年化）
    w_A = 0.6
    w_B = 0.4
    weights = np.array([w_A, w_B])

    # 相关系数
    rho_before = 0.3
    rho_after  = 0.8

    # 协方差矩阵计算函数
    def cov_matrix(sigma1, sigma2, rho):
        cov = rho * sigma1 * sigma2
        return np.array([[sigma1**2, cov],
                         [cov, sigma2**2]])

    # 计算组合波动率（年化标准差）
    def portfolio_vol(weights, cov_mat):
        return np.sqrt(weights.T @ cov_mat @ weights)

    # 变化前的协方差矩阵与波动率
    cov_before = cov_matrix(sigma_A, sigma_B, rho_before)
    vol_before = portfolio_vol(weights, cov_before)

    # 变化后的协方差矩阵与波动率
    cov_after = cov_matrix(sigma_A, sigma_B, rho_after)
    vol_after = portfolio_vol(weights, cov_after)

    # 存储结果
    result = {
        'vol_before_annual': vol_before,
        'vol_after_annual': vol_after
    }

    # 打印结果（方便投屏显示）
    print("=== 组合波动率计算 ===")
    print(f"资产A波动率: {sigma_A*100:.1f}%")
    print(f"资产B波动率: {sigma_B*100:.1f}%")
    print(f"权重: A={w_A*100:.0f}%, B={w_B*100:.0f}%")
    print(f"相关系数 0.3 时的组合波动率: {vol_before*100:.2f}%")
    print(f"相关系数 0.8 时的组合波动率: {vol_after*100:.2f}%")
    print("\n结果字典:", result)

    return result

if __name__ == "__main__":
    main()
