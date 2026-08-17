import numpy as np

# ============================================
# 《证券投资学》课堂实时编程：马科维茨最小方差组合
# ============================================

def compute_mvp():
    # 1. 由波动率与相关系数构造协方差矩阵
    vols = np.array([0.187, 0.243, 0.312])
    corr_matrix = np.array([
        [1.0, 0.21, -0.13],
        [0.21, 1.0, 0.37],
        [-0.13, 0.37, 1.0]
    ])
    
    # 协方差矩阵 Sigma = diag(vol) @ Corr @ diag(vol)
    Sigma = np.diag(vols) @ corr_matrix @ np.diag(vols)
    
    # 2. 求最小方差权重（闭式解），归一化使其和为 1
    # 满仓约束下，全局最小方差组合权重 w = (Sigma^-1 * 1) / (1' * Sigma^-1 * 1)
    ones = np.ones(3)
    # 使用线性方程组求解代替直接求逆，数值稳定性更好
    Sigma_inv_ones = np.linalg.solve(Sigma, ones)
    mvp_weights = Sigma_inv_ones / np.sum(Sigma_inv_ones)
    
    # 3. 组合波动率取 w'Σw 的平方根
    mvp_var = mvp_weights.T @ Sigma @ mvp_weights
    mvp_vol_annual = np.sqrt(mvp_var)
    
    # 4. 按要求键名填充 result
    result = {
        'mvp_weights': mvp_weights,
        'mvp_vol_annual': mvp_vol_annual
    }
    
    return result

if __name__ == '__main__':
    result = compute_mvp()
    
    # 格式化输出，便于课堂投屏展示
    print("=== 马科维茨全局最小方差组合 (MVP) ===")
    print(f"权重分配 (资产1, 资产2, 资产3): {result['mvp_weights']}")
    print(f"年化波动率: {result['mvp_vol_annual']:.4f} (即 {result['mvp_vol_annual']*100:.2f}%)")
    print("\n原始返回字典结果：")
    print(result)
