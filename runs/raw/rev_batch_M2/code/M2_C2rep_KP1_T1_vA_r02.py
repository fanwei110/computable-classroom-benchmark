import numpy as np

def main():
    # 给定的年化波动率
    sigmas = np.array([0.187, 0.243, 0.312])
    # 相关系数矩阵
    corr = np.array([
        [1.00, 0.21, -0.13],
        [0.21, 1.00,  0.37],
        [-0.13,0.37,  1.00]
    ])
    
    # 1. 构造协方差矩阵
    # Σ = diag(sigmas) @ corr @ diag(sigmas)
    D = np.diag(sigmas)
    Sigma = D @ corr @ D
    
    # 2. 全局最小方差权重（允许卖空，权重之和为1）
    # 闭式解：w = (Σ^{-1} * 1) / (1^T * Σ^{-1} * 1)
    inv_Sigma = np.linalg.inv(Sigma)
    ones = np.ones(len(sigmas))
    numerator = inv_Sigma @ ones
    denominator = ones @ numerator
    w_mvp = numerator / denominator
    
    # 3. 组合年化波动率
    # σ_p = sqrt(w^T Σ w)
    var_p = w_mvp @ Sigma @ w_mvp
    sigma_p = np.sqrt(var_p)
    
    # 4. 存入结果字典
    result = {
        'mvp_weights': w_mvp.tolist(),
        'mvp_vol_annual': sigma_p
    }
    
    # 输出结果（满足课堂展示需求）
    print("全局最小方差组合结果：")
    print(f"权重：{result['mvp_weights']}")
    print(f"年化波动率：{result['mvp_vol_annual']:.6f}")
    
    return result

if __name__ == "__main__":
    result = main()
