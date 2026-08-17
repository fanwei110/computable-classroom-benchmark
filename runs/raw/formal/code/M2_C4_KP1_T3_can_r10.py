import numpy as np

def main():
    # 资产波动率（小数）
    sigma_A = 0.184   # 资产 A 年化波动率 18.4%
    sigma_B = 0.297   # 资产 B 年化波动率 29.7%

    # 组合权重（A 占 60%，B 占 40%）
    w_A = 0.6
    w_B = 0.4

    # 相关系数
    rho_before = 0.3
    rho_after  = 0.8

    # 协方差（协方差 = 相关系数 * 标准差之积）
    cov_before = rho_before * sigma_A * sigma_B
    cov_after  = rho_after  * sigma_A * sigma_B

    # 组合方差： w_A^2 * σ_A^2 + w_B^2 * σ_B^2 + 2 * w_A * w_B * Cov(A,B)
    var_before = (w_A**2 * sigma_A**2 +
                  w_B**2 * sigma_B**2 +
                  2 * w_A * w_B * cov_before)
    var_after  = (w_A**2 * sigma_A**2 +
                  w_B**2 * sigma_B**2 +
                  2 * w_A * w_B * cov_after)

    # 组合波动率（年化，小数）
    vol_before = np.sqrt(var_before)
    vol_after  = np.sqrt(var_after)

    # 按要求输出到 result 字典
    result = {
        'vol_before_annual': vol_before,
        'vol_after_annual': vol_after
    }

    print("组合波动率（年化，小数）:")
    print(f"  相关系数 0.3 时: {vol_before:.6f} ({vol_before*100:.4f}%)")
    print(f"  相关系数 0.8 时: {vol_after:.6f}  ({vol_after*100:.4f}%)")
    return result

# 执行主函数并生成全局变量 result
result = main()
