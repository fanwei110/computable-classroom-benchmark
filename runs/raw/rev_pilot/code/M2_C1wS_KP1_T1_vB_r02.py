import numpy as np

def main():
    # 给定数据
    vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
    # 相关系数矩阵（下三角给出，补全为对称矩阵）
    corr = np.array([
        [1.0,  0.21, -0.13],
        [0.21, 1.0,   0.37],
        [-0.13, 0.37,  1.0 ]
    ])

    # 1. 构建协方差矩阵
    Sigma = np.outer(vols, vols) * corr

    # 2. 计算最小方差组合权重（允许做空，满仓，权重和为1）
    inv_Sigma = np.linalg.inv(Sigma)
    ones = np.ones(len(vols))
    # 权重公式: w = (Σ^{-1} * 1) / (1^T * Σ^{-1} * 1)
    mvp_weights = inv_Sigma @ ones / (ones @ inv_Sigma @ ones)

    # 3. 组合年化波动率 = sqrt(w' Σ w)
    var_mvp = mvp_weights @ Sigma @ mvp_weights
    mvp_vol = np.sqrt(var_mvp)

    # 4. 汇总结果
    result = {
        'mvp_weights': mvp_weights.tolist(),
        'mvp_vol_annual': mvp_vol
    }

    # 输出至控制台（便于投屏查看）
    print("=== 最小方差组合 (MVP) 结果 ===")
    print(f"资产波动率: {vols}")
    print(f"相关系数矩阵:\n{corr}")
    print(f"协方差矩阵:\n{Sigma}")
    print(f"最优权重: {mvp_weights}")
    print(f"组合年化波动率: {mvp_vol:.4%}")
    print("\n存储的 result 字典:")
    print(result)

    return result

if __name__ == "__main__":
    res = main()
