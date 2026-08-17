import numpy as np

def main():
    # 1. 给定数据
    # 年化波动率（小数）
    sigma = np.array([0.187, 0.243, 0.312])
    
    # 相关系数矩阵
    corr = np.array([
        [1.00, 0.21, -0.13],
        [0.21, 1.00,  0.37],
        [-0.13, 0.37, 1.00]
    ])
    
    # 2. 构造协方差矩阵
    # cov(i,j) = corr(i,j) * sigma(i) * sigma(j)
    Sigma = np.outer(sigma, sigma) * corr
    
    # 3. 全局最小方差组合权重（允许卖空，满仓）
    # 解析解：w = (Σ^{-1} * 1) / (1' * Σ^{-1} * 1)
    # 其中 1 为全1向量
    
    n = len(sigma)
    ones = np.ones(n)
    
    # 计算协方差矩阵的逆
    Sigma_inv = np.linalg.inv(Sigma)
    
    # 计算未归一化权重
    w_unnorm = Sigma_inv @ ones
    
    # 归一化使权重和为1
    w_mvp = w_unnorm / (ones @ w_unnorm)
    
    # 4. 计算组合年化波动率
    # 组合方差 = w' Σ w
    var_mvp = w_mvp @ Sigma @ w_mvp
    vol_mvp = np.sqrt(var_mvp)
    
    # 5. 构建结果字典
    result = {
        'mvp_weights': w_mvp.tolist(),
        'mvp_vol_annual': float(vol_mvp)
    }
    
    # 打印结果以供验证
    print("全局最小方差组合 (Global MVP)")
    print(f"权重: {w_mvp}")
    print(f"权重和: {np.sum(w_mvp):.8f}")
    print(f"年化波动率: {vol_mvp:.6f} ({vol_mvp*100:.4f}%)")
    
    return result

if __name__ == "__main__":
    result = main()
