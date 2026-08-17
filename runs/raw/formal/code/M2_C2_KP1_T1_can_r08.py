import numpy as np

# 给定数据
vol = np.array([0.187, 0.243, 0.312])          # 年化波动率
corr = np.array([[ 1.  ,  0.21, -0.13],
                 [ 0.21,  1.  ,  0.37],
                 [-0.13,  0.37,  1.  ]])        # 相关系数矩阵

# 1. 构造协方差矩阵
cov = np.outer(vol, vol) * corr

# 2. 全局最小方差组合权重（允许卖空，满仓约束）
inv_cov = np.linalg.inv(cov)
ones = np.ones(len(vol))
w_mvp = inv_cov @ ones / (ones @ inv_cov @ ones)

# 3. 组合年化波动率
mvp_vol = np.sqrt(w_mvp @ cov @ w_mvp)

# 4. 输出契约
result = {
    'mvp_weights': w_mvp.tolist(),   # 转为列表，方便展示
    'mvp_vol_annual': float(mvp_vol)
}

if __name__ == "__main__":
    print("全局最小方差组合结果：")
    print(f"权重: {result['mvp_weights']}")
    print(f"年化波动率: {result['mvp_vol_annual']:.4f} ({result['mvp_vol_annual']*100:.2f}%)")
