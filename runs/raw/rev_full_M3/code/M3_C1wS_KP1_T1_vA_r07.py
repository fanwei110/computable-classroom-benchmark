import numpy as np

# ==================== 1. 输入数据 ====================
# 年化波动率
vols = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr = np.array([
    [1.0,  0.21, -0.13],
    [0.21, 1.0,   0.37],
    [-0.13, 0.37, 1.0 ]
])

# ==================== 2. 构造协方差矩阵 ====================
# 协方差矩阵 Σ = diag(σ) @ Corr @ diag(σ)
cov_matrix = np.outer(vols, vols) * corr

# ==================== 3. 求最小方差组合权重 ====================
# 允许卖空且满仓约束下，最小方差组合权重的闭式解为：
# w_mvp = (Σ^{-1} @ 1) / (1' @ Σ^{-1} @ 1)
ones = np.ones(3)
inv_cov = np.linalg.inv(cov_matrix)

w_mvp = (inv_cov @ ones) / (ones @ inv_cov @ ones)

# ==================== 4. 计算组合的年化波动率 ====================
# 组合方差 = w' Σ w，组合波动率为其平方根
var_mvp = w_mvp @ cov_matrix @ w_mvp
vol_mvp = np.sqrt(var_mvp)

# ==================== 5. 按要求封装结果 ====================
result = {
    'mvp_weights': w_mvp.tolist(),  # 转为原生list便于展示与序列化
    'mvp_vol_annual': float(vol_mvp) # 转为原生float
}

# 课堂投屏展示打印
if __name__ == '__main__':
    print("=== 马科维茨最小方差组合计算结果 ===")
    print(f"资产权重: {result['mvp_weights']}")
    print(f"组合年化波动率: {result['mvp_vol_annual']:.4%}")
