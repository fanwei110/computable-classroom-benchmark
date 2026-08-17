import numpy as np

def main():
    # === 1. 参数设定 ===
    # 资产 A 权重 60%，资产 B 权重 40%
    w_A = 0.6
    w_B = 0.4

    # 两资产的年化波动率（标准差）
    sigma_A = 0.184  # 18.4%
    sigma_B = 0.297  # 29.7%

    # 相关系数：变化前和变化后
    rho_before = 0.3
    rho_after  = 0.8

    # === 2. 构造协方差矩阵 ===
    # 协方差公式: cov(A,B) = rho * sigma_A * sigma_B
    cov_before = rho_before * sigma_A * sigma_B
    cov_after  = rho_after  * sigma_A * sigma_B

    # 协方差矩阵（2x2）
    # 对角线: 方差 sigma^2
    # 非对角线: 协方差
    Sigma_before = np.array([[sigma_A**2, cov_before],
                             [cov_before, sigma_B**2]])

    Sigma_after  = np.array([[sigma_A**2, cov_after],
                             [cov_after,  sigma_B**2]])

    # === 3. 计算组合波动率 ===
    # 组合方差公式: w' Σ w
    w = np.array([w_A, w_B])

    var_before = w.T @ Sigma_before @ w
    var_after  = w.T @ Sigma_after  @ w

    # 波动率 = sqrt(方差)
    vol_before_annual = np.sqrt(var_before)
    vol_after_annual  = np.sqrt(var_after)

    # === 4. 填充结果字典 ===
    result = {
        'vol_before_annual': vol_before_annual,
        'vol_after_annual': vol_after_annual
    }

    # 控制台输出，便于课堂查看
    print("=== 马科维茨两资产组合波动率计算 ===")
    print(f"资产A: 权重 {w_A*100:.0f}%, 波动率 {sigma_A*100:.1f}%")
    print(f"资产B: 权重 {w_B*100:.0f}%, 波动率 {sigma_B*100:.1f}%")
    print(f"组合波动率 (ρ=0.3): {vol_before_annual*100:.2f}%")
    print(f"组合波动率 (ρ=0.8): {vol_after_annual*100:.2f}%")
    print("\n结果字典:")
    print(result)

    return result

if __name__ == "__main__":
    result = main()
