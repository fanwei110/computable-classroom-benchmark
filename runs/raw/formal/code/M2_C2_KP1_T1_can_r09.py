import numpy as np

def compute_mvp():
    # 年化波动率
    sigma = np.array([0.187, 0.243, 0.312])
    # 相关系数矩阵
    corr = np.array([
        [ 1.00,  0.21, -0.13],
        [ 0.21,  1.00,  0.37],
        [-0.13,  0.37,  1.00]
    ])
    # 构造协方差矩阵: Σ_ij = σ_i * σ_j * ρ_ij
    Sigma = np.outer(sigma, sigma) * corr

    # 全局最小方差组合权重（允许卖空，满仓）: w = (Σ^{-1} * 1) / (1^T * Σ^{-1} * 1)
    inv_Sigma = np.linalg.inv(Sigma)
    ones = np.ones(3)
    w = inv_Sigma @ ones / (ones @ inv_Sigma @ ones)

    # 组合年化波动率: sqrt(w^T Σ w)
    var_port = w @ Sigma @ w
    vol_port = np.sqrt(var_port)

    # 输出结果
    result = {
        'mvp_weights': w,
        'mvp_vol_annual': vol_port
    }
    return result

if __name__ == '__main__':
    result = compute_mvp()
    print("全局最小方差组合结果：")
    print(f"权重: {result['mvp_weights']}")
    print(f"年化波动率: {result['mvp_vol_annual']:.4f}")
