import numpy as np

def main():
    """
    计算三资产全局最小方差组合（允许卖空，全额投资）
    """
    # 给定年化波动率（小数形式）
    sigma = np.array([0.187, 0.243, 0.312])
    
    # 给定相关系数矩阵
    corr_matrix = np.array([
        [1.00,  0.21, -0.13],
        [0.21,  1.00,  0.37],
        [-0.13, 0.37,  1.00]
    ])
    
    # 1. 构造协方差矩阵 Σ
    # Σ[i,j] = corr(i,j) * sigma_i * sigma_j
    D = np.diag(sigma)  # 对角矩阵，对角线为各资产波动率
    cov_matrix = D @ corr_matrix @ D  # 等价于 D * corr * D
    
    # 2. 计算全局最小方差组合权重（闭式解）
    # 问题：min w' Σ w ,  s.t. 1' w = 1
    # 闭式解：w_mvp = Σ^{-1} 1 / (1' Σ^{-1} 1)
    inv_cov = np.linalg.inv(cov_matrix)
    ones = np.ones(3)
    
    numerator = inv_cov @ ones               # Σ^{-1} 1
    denominator = ones @ inv_cov @ ones      # 1' Σ^{-1} 1
    
    w_mvp = numerator / denominator
    
    # 3. 计算组合年化波动率
    # σ_p = sqrt(w' Σ w)
    var_mvp = w_mvp @ cov_matrix @ w_mvp
    vol_mvp = np.sqrt(var_mvp)
    
    # 4. 填充结果字典
    result = {
        'mvp_weights': w_mvp.tolist(),
        'mvp_vol_annual': float(vol_mvp)
    }
    
    # 打印结果，便于课堂展示
    print("协方差矩阵 Σ:")
    print(np.array2string(cov_matrix, precision=6, suppress_small=True))
    print("\n全局最小方差组合权重:")
    for i, w in enumerate(w_mvp):
        print(f"  资产 {i+1}: {w:.4f} ({w*100:.2f}%)")
    print(f"  权重和: {np.sum(w_mvp):.6f}")
    print(f"\n组合年化波动率 (MVP): {vol_mvp:.6f}  ({vol_mvp*100:.4f}%)")
    
    return result

# 直接运行以验证
if __name__ == "__main__":
    result = main()
