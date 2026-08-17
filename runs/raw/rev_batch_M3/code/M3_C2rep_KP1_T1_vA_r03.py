import numpy as np

def main():
    # ===================== 1. 由波动率与相关系数构造协方差矩阵 =====================
    # 年化波动率
    vols = np.array([0.187, 0.243, 0.312])
    
    # 相关系数矩阵
    corr = np.array([
        [1.0,  0.21, -0.13],
        [0.21, 1.0,   0.37],
        [-0.13, 0.37, 1.0 ]
    ])
    
    # 协方差矩阵 Sigma = diag(vol) @ Corr @ diag(vol) 等价于外积逐元素乘
    cov_matrix = np.outer(vols, vols) * corr

    # ===================== 2. 求最小方差权重 =====================
    # 全局最小方差组合(GMVP)的闭式解：w = (Sigma^-1 @ 1) / (1^T @ Sigma^-1 @ 1)
    ones = np.ones(3)
    inv_cov = np.linalg.inv(cov_matrix)
    
    # 计算闭式解权重，自然满足 sum(w) = 1
    w_mvp = (inv_cov @ ones) / (ones @ inv_cov @ ones)

    # ===================== 3. 组合波动率取 w'Σw 的平方根 =====================
    var_mvp = w_mvp.T @ cov_matrix @ w_mvp
    vol_mvp = np.sqrt(var_mvp)

    # ===================== 4. 按要求键名填充 result =====================
    result = {
        'mvp_weights': w_mvp.tolist(),   # 转为list便于跨环境序列化展示
        'mvp_vol_annual': float(vol_mvp) # 转为Python原生float
    }
    
    # 打印结果供课堂投屏展示
    print("全局最小方差组合结果：")
    print(f"权重: {result['mvp_weights']}")
    print(f"年化波动率: {result['mvp_vol_annual']:.4f} (即 {result['mvp_vol_annual']*100:.2f}%)")
    
    return result

if __name__ == '__main__':
    result = main()
