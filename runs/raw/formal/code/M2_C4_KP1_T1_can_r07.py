import numpy as np

def main():
    # 给定的年化波动率
    sigmas = np.array([0.187, 0.243, 0.312])
    # 给定的相关系数矩阵（对称）
    corr = np.array([
        [1.0,  0.21, -0.13],
        [0.21, 1.0,   0.37],
        [-0.13, 0.37,  1.0]
    ])
    
    # 1. 构造协方差矩阵
    # Σ[i][j] = σ_i * σ_j * ρ_ij
    cov = np.outer(sigmas, sigmas) * corr
    
    # 2. 计算最小方差组合权重（允许卖空，权重和为1）
    # 闭式解: w = (Σ^{-1} 1) / (1^T Σ^{-1} 1)
    inv_cov = np.linalg.inv(cov)
    ones = np.ones(3)
    numerator = inv_cov @ ones
    denominator = ones @ numerator
    w_mvp = numerator / denominator
    
    # 3. 组合年化波动率
    var_mvp = w_mvp @ cov @ w_mvp
    vol_mvp = np.sqrt(var_mvp)
    
    # 4. 按契约构建结果字典
    result = {
        'mvp_weights': w_mvp.tolist(),   # 转为列表，便于阅读
        'mvp_vol_annual': float(vol_mvp)
    }
    
    # 打印结果，方便教师投屏查看
    print("全局最小方差组合（允许卖空）")
    print(f"权重: {w_mvp}")
    print(f"年化波动率: {vol_mvp:.6f} ({vol_mvp*100:.4f}%)")
    print("\n结果字典:")
    print(result)
    
    return result

if __name__ == "__main__":
    main()
