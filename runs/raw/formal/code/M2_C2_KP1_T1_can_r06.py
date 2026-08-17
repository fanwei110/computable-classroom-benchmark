import numpy as np

def main():
    # 年化波动率
    sigma = np.array([0.187, 0.243, 0.312])
    
    # 相关系数矩阵（对称矩阵）
    corr = np.array([
        [1.0,  0.21, -0.13],
        [0.21, 1.0,   0.37],
        [-0.13, 0.37,  1.0 ]
    ])
    
    # 构造协方差矩阵：cov[i,j] = sigma[i] * sigma[j] * corr[i,j]
    cov = np.outer(sigma, sigma) * corr
    
    # 求协方差矩阵的逆
    inv_cov = np.linalg.inv(cov)
    
    # 全1向量
    ones = np.ones(3)
    
    # 最小方差组合权重（闭式解）：w = inv_cov @ ones / (ones' @ inv_cov @ ones)
    numerator = inv_cov @ ones
    denominator = ones @ numerator
    weights = numerator / denominator
    
    # 组合方差 = 1 / (ones' @ inv_cov @ ones)
    port_var = 1.0 / denominator
    
    # 组合年化波动率
    port_vol = np.sqrt(port_var)
    
    # 按要求存放结果
    result = {
        'mvp_weights': weights.tolist(),
        'mvp_vol_annual': port_vol
    }
    
    # 输出结果（便于课堂投屏查看）
    print("全局最小方差组合（允许卖空，满仓）")
    print(f"权重: {result['mvp_weights']}")
    print(f"年化波动率: {result['mvp_vol_annual']:.6f} ({result['mvp_vol_annual']*100:.4f}%)")
    
    return result

if __name__ == "__main__":
    result = main()
