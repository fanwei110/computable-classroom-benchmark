import numpy as np

def main():
    # 1. 配置资产参数与权重
    # 资产A权重60%，资产B权重40%
    weights = np.array([0.6, 0.4])
    
    # 年化波动率（标准差）
    vol_A_annual = 0.184  # 资产A年化波动率18.4%
    vol_B_annual = 0.297  # 资产B年化波动率29.7%
    
    # 2. 构造两个相关系数下的协方差矩阵
    # 协方差公式：cov(i,j) = rho * sigma_i * sigma_j
    def build_cov_matrix(rho):
        cov_AB = rho * vol_A_annual * vol_B_annual
        cov_matrix = np.array([
            [vol_A_annual**2, cov_AB],
            [cov_AB, vol_B_annual**2]
        ])
        return cov_matrix
    
    cov_before = build_cov_matrix(0.3)  # 相关系数0.3
    cov_after  = build_cov_matrix(0.8)  # 相关系数0.8
    
    # 3. 计算组合年化波动率
    # 组合方差 = w' * Σ * w
    portfolio_variance_before = weights.T @ cov_before @ weights
    portfolio_variance_after  = weights.T @ cov_after @ weights
    
    # 组合年化波动率（标准差）
    vol_before_annual = np.sqrt(portfolio_variance_before)
    vol_after_annual  = np.sqrt(portfolio_variance_after)
    
    # 4. 存储结果
    result = {
        'vol_before_annual': vol_before_annual,
        'vol_after_annual': vol_after_annual
    }
    
    # 输出结果供查看（符合课堂演示要求）
    print("=== 60/40 组合波动率变化分析 ===")
    print(f"资产A年化波动率: {vol_A_annual*100:.1f}%")
    print(f"资产B年化波动率: {vol_B_annual*100:.1f}%")
    print(f"权重: A={weights[0]*100:.0f}%, B={weights[1]*100:.0f}%")
    print(f"\n相关系数 0.3 时组合年化波动率: {vol_before_annual*100:.2f}%")
    print(f"相关系数 0.8 时组合年化波动率: {vol_after_annual*100:.2f}%")
    print(f"波动率变化: {(vol_after_annual - vol_before_annual)*100:.2f} 个百分点")
    
    # 返回 result 字典（符合题目输出契约）
    return result

if __name__ == "__main__":
    result = main()

