import numpy as np

def main():
    # 给定的资产年化波动率（小数表示）
    sigma_A = 0.184   # 18.4%
    sigma_B = 0.297   # 29.7%

    # 组合权重，按“A和B的60/40组合”对应 A=60%, B=40%
    w_A = 0.6
    w_B = 0.4
    weights = np.array([w_A, w_B])

    # 两个相关系数
    rho_before = 0.3
    rho_after  = 0.8

    # 构造协方差矩阵：[[σ_A^2, ρσ_Aσ_B], [ρσ_Aσ_B, σ_B^2]]
    cov_before = np.array([
        [sigma_A**2,               rho_before * sigma_A * sigma_B],
        [rho_before * sigma_A * sigma_B, sigma_B**2]
    ])
    cov_after = np.array([
        [sigma_A**2,               rho_after * sigma_A * sigma_B],
        [rho_after * sigma_A * sigma_B, sigma_B**2]
    ])

    # 组合方差 = w' Σ w
    var_before = weights @ cov_before @ weights
    var_after  = weights @ cov_after  @ weights

    # 组合年化波动率
    vol_before = np.sqrt(var_before)
    vol_after  = np.sqrt(var_after)

    # 按要求的键名填入结果字典
    result = {
        'vol_before_annual': vol_before,
        'vol_after_annual':  vol_after
    }

    # 屏幕上输出，便于课堂实时查看
    print("=== 60/40 组合的波动率变化 ===")
    print(f"相关系数 0.3 时组合年化波动率: {vol_before:.4f} ({vol_before*100:.2f}%)")
    print(f"相关系数 0.8 时组合年化波动率: {vol_after:.4f} ({vol_after*100:.2f}%)")
    print("\n结果字典：", result)

if __name__ == "__main__":
    main()
