import numpy as np

def main():
    # 年化波动率
    sigma = np.array([0.187, 0.243, 0.312])
    
    # 相关系数矩阵
    corr = np.array([
        [1.0,  0.21, -0.13],
        [0.21, 1.0,   0.37],
        [-0.13,0.37,  1.0 ]
    ])
    
    # 构建年化协方差矩阵
    cov = np.outer(sigma, sigma) * corr
    
    # 全局最小方差组合 (允许卖空，资金全部投出 -> 权重和为1)
    inv_cov = np.linalg.inv(cov)
    ones = np.ones(len(sigma))
    mvp_weights = inv_cov @ ones / (ones @ inv_cov @ ones)
    
    # 组合年化波动率
    mvp_var = mvp_weights @ cov @ mvp_weights
    mvp_vol_annual = np.sqrt(mvp_var)
    
    # 存入结果字典，键名严格给定
    result = {
        'mvp_weights': mvp_weights.tolist(),
        'mvp_vol_annual': float(mvp_vol_annual)
    }
    
    # 可选：将结果打印到控制台，方便查看
    print("全局最小方差组合结果：")
    print(f"权重: {result['mvp_weights']}")
    print(f"年化波动率: {result['mvp_vol_annual']:.4f}")
    
    return result

if __name__ == "__main__":
    result = main()
