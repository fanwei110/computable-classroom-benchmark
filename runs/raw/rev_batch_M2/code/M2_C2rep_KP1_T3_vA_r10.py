import numpy as np

def main():
    # 1. 自行确定 60/40 权重与两只资产的对应方式。
    # 假设资产 A 权重 60%，资产 B 权重 40%
    w_a = 0.60
    w_b = 0.40
    weights = np.array([w_a, w_b])
    
    # 资产 A 的年化波动率大约 18.4%，资产 B 大约 29.7%
    sigma_a = 0.184
    sigma_b = 0.297
    
    # 2. 构造相关系数 0.3 与 0.8 两个协方差矩阵
    rho_before = 0.3
    rho_after = 0.8
    
    # 协方差计算公式: cov(i,j) = rho * sigma_i * sigma_j
    cov_ab_before = rho_before * sigma_a * sigma_b
    cov_ab_after = rho_after * sigma_a * sigma_b
    
    var_a = sigma_a**2
    var_b = sigma_b**2
    
    cov_matrix_before = np.array([
        [var_a, cov_ab_before],
        [cov_ab_before, var_b]
    ])
    
    cov_matrix_after = np.array([
        [var_a, cov_ab_after],
        [cov_ab_after, var_b]
    ])
    
    # 3. 计算两个组合波动率
    # 组合方差: w'Σw
    port_variance_before = weights @ cov_matrix_before @ weights
    port_variance_after = weights @ cov_matrix_after @ weights
    
    # 年化波动率 = sqrt(组合方差)
    vol_before_annual = np.sqrt(port_variance_before)
    vol_after_annual = np.sqrt(port_variance_after)
    
    # 4. 填充 result
    result = {
        'vol_before_annual': vol_before_annual,
        'vol_after_annual': vol_after_annual
    }
    
    # 输出结果，便于教师查看
    print(f"资产A权重: {w_a*100:.0f}%, 资产B权重: {w_b*100:.0f}%")
    print(f"资产A年化波动率: {sigma_a*100:.1f}%")
    print(f"资产B年化波动率: {sigma_b*100:.1f}%")
    print(f"相关系数0.3时组合年化波动率: {vol_before_annual*100:.2f}%")
    print(f"相关系数0.8时组合年化波动率: {vol_after_annual*100:.2f}%")
    print(f"波动率变化: {(vol_after_annual - vol_before_annual)*100:.2f}个百分点")
    print(f"\n结果字典: {result}")
    
    return result

if __name__ == "__main__":
    result = main()
