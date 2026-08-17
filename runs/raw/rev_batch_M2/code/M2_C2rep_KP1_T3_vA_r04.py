import numpy as np

def main():
    # 资产年化波动率（标准差）
    sigma_A = 0.184  # 18.4%
    sigma_B = 0.297  # 29.7%

    # 60/40 组合权重：假设 60% 资产 A，40% 资产 B
    w = np.array([0.6, 0.4])

    # 两个相关系数情景
    rho_before = 0.3
    rho_after  = 0.8

    # 构造协方差矩阵的函数
    def cov_matrix(sigma1, sigma2, rho):
        cov = rho * sigma1 * sigma2
        return np.array([[sigma1**2, cov],
                         [cov, sigma2**2]])

    # 情景1: 相关系数 0.3
    Sigma_before = cov_matrix(sigma_A, sigma_B, rho_before)
    var_before = w.T @ Sigma_before @ w
    vol_before = np.sqrt(var_before)

    # 情景2: 相关系数 0.8
    Sigma_after = cov_matrix(sigma_A, sigma_B, rho_after)
    var_after = w.T @ Sigma_after @ w
    vol_after = np.sqrt(var_after)

    # 存放结果
    result = {
        'vol_before_annual': vol_before,
        'vol_after_annual': vol_after
    }

    # 输出结果（用于课堂投屏）
    print("=== 马科维茨均值-方差分析：60/40 组合波动率 ===")
    print(f"资产 A 年化波动率: {sigma_A*100:.1f}%")
    print(f"资产 B 年化波动率: {sigma_B*100:.1f}%")
    print(f"权重: A={w[0]*100:.0f}%, B={w[1]*100:.0f}%")
    print(f"相关系数 {rho_before} 时组合年化波动率: {vol_before*100:.2f}%")
    print(f"相关系数 {rho_after} 时组合年化波动率: {vol_after*100:.2f}%")
    print(f"波动率变化: {(vol_after - vol_before)*100:.2f} 个百分点")
    print("\n结果字典:")
    print(result)

    return result

if __name__ == "__main__":
    result = main()
