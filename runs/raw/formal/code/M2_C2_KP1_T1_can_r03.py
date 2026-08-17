import numpy as np

def main():
    # 年化波动率
    sigmas = np.array([0.187, 0.243, 0.312])
    # 相关系数矩阵（下三角按顺序给出，先构建完整矩阵）
    corr = np.array([
        [1.00, 0.21, -0.13],
        [0.21, 1.00,  0.37],
        [-0.13, 0.37, 1.00]
    ])
    # 1. 构造协方差矩阵： Sigma = D * corr * D, D是对角矩阵
    Sigma = np.diag(sigmas) @ corr @ np.diag(sigmas)

    # 2. 全局最小方差组合权重（允许卖空，满仓）
    # 闭式解： w_mvp = (Sigma^{-1} * 1) / (1^T * Sigma^{-1} * 1)
    ones = np.ones(len(sigmas))
    Sigma_inv = np.linalg.inv(Sigma)
    w_mvp = Sigma_inv @ ones / (ones @ Sigma_inv @ ones)

    # 3. 组合年化波动率
    mvp_var = w_mvp @ Sigma @ w_mvp
    mvp_vol = np.sqrt(mvp_var)

    # 4. 按要求存入字典
    result = {
        'mvp_weights': w_mvp.tolist(),  # 转为列表便于查看
        'mvp_vol_annual': mvp_vol
    }

    # 输出到控制台供教师查看
    print("全局最小方差组合权重:", result['mvp_weights'])
    print("年化波动率:", result['mvp_vol_annual'])

    return result

# 运行脚本
if __name__ == "__main__":
    result = main()
