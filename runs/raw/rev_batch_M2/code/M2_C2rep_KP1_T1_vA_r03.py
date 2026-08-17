import numpy as np

def main():
    # 给定的年化波动率
    sigmas = np.array([0.187, 0.243, 0.312])
    # 给定的相关系数矩阵
    corr = np.array([
        [1.0,  0.21, -0.13],
        [0.21, 1.0,   0.37],
        [-0.13, 0.37,  1.0]
    ])
    
    # 1. 构造协方差矩阵
    Sigma = np.diag(sigmas) @ corr @ np.diag(sigmas)
    # 等价于：Sigma[i,j] = sigmas[i]*sigmas[j]*corr[i,j]
    
    # 2. 求最小方差组合权重（闭合解，满仓约束 w'1 = 1）
    ones = np.ones(3)
    Sigma_inv = np.linalg.inv(Sigma)
    # 未归一化的权重：Σ^-1 * 1
    # 归一化因子：1' * Σ^-1 * 1
    mvp_weights = Sigma_inv @ ones / (ones @ Sigma_inv @ ones)
    
    # 3. 组合年化波动率 (w' Σ w)^0.5
    mvp_var = mvp_weights @ Sigma @ mvp_weights
    mvp_vol_annual = np.sqrt(mvp_var)
    
    # 4. 按要求输出字典
    result = {
        'mvp_weights': mvp_weights.tolist(),  # 转换为list以防numpy数组不可序列化
        'mvp_vol_annual': float(mvp_vol_annual)
    }
    
    # 打印结果以便投屏查看（同时保留字典变量）
    print("全局最小方差组合结果：")
    print(f"权重: {result['mvp_weights']}")
    print(f"年化波动率: {result['mvp_vol_annual']:.4f}")

if __name__ == "__main__":
    main()
