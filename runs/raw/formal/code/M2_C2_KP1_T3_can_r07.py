import numpy as np

def main():
    # 年化波动率（标准差）
    sigma_A = 0.184  # 资产A的年化波动率
    sigma_B = 0.297  # 资产B的年化波动率

    # 组合权重：60/40，此处定义 A 占 60%，B 占 40%
    w_A = 0.6
    w_B = 0.4
    weights = np.array([w_A, w_B])

    # 相关系数
    rho_before = 0.3
    rho_after  = 0.8

    # 协方差矩阵函数
    def cov_matrix(rho):
        cov = np.array([[sigma_A**2, rho * sigma_A * sigma_B],
                        [rho * sigma_A * sigma_B, sigma_B**2]])
        return cov

    # 计算组合波动率：σ_p = sqrt(w' Σ w)
    def portfolio_vol(rho):
        cov = cov_matrix(rho)
        var = weights.T @ cov @ weights
        return np.sqrt(var)

    vol_before = portfolio_vol(rho_before)
    vol_after  = portfolio_vol(rho_after)

    # 结果字典
    result = {
        'vol_before_annual': vol_before,
        'vol_after_annual': vol_after
    }

    # 打印结果，便于课堂投屏展示
    print("=== 马科维茨均值-方差组合分析 ===")
    print(f"资产A年化波动率: {sigma_A:.1%}")
    print(f"资产B年化波动率: {sigma_B:.1%}")
    print(f"组合权重: A={w_A:.0%}, B={w_B:.0%}")
    print(f"相关系数 0.3 时组合年化波动率: {vol_before:.4f} ({vol_before:.2%})")
    print(f"相关系数 0.8 时组合年化波动率: {vol_after:.4f} ({vol_after:.2%})")
    print("波动率变动: {:.4f}".format(vol_after - vol_before))
    print("\n结果字典 result =")
    print(result)

    return result

if __name__ == "__main__":
    main()
