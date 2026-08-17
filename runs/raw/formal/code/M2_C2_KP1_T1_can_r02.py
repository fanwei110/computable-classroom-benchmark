import numpy as np

def compute_gmvp():
    # 年化波动率
    sigmas = np.array([0.187, 0.243, 0.312])
    # 相关系数矩阵
    corr = np.array([
        [1.00, 0.21, -0.13],
        [0.21, 1.00,  0.37],
        [-0.13, 0.37,  1.00]
    ])
    
    # 1. 协方差矩阵
    Sigma = np.diag(sigmas) @ corr @ np.diag(sigmas)
    
    # 2. 最小方差组合权重（闭式解，允许卖空，满仓）
    ones = np.ones(len(sigmas))
    Sigma_inv = np.linalg.inv(Sigma)
    # w* = (Σ^{-1} 1) / (1' Σ^{-1} 1)
    w_mvp = Sigma_inv @ ones / (ones @ Sigma_inv @ ones)
    
    # 3. 组合年化波动率
    var_mvp = w_mvp @ Sigma @ w_mvp
    vol_mvp = np.sqrt(var_mvp)
    
    # 4. 按要求键名填充结果
    result = {
        'mvp_weights': w_mvp.tolist(),   # 转为列表，方便查看
        'mvp_vol_annual': vol_mvp
    }
    
    return result

if __name__ == "__main__":
    result = compute_gmvp()
    # 输出 result 字典供课堂投屏
    print("全局最小方差组合结果：")
    print(f"权重: {result['mvp_weights']}")
    print(f"年化波动率: {result['mvp_vol_annual']:.6f}")
