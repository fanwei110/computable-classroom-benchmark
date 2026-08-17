import numpy as np

# ==================== 1. 参数设定 ====================
# 年化波动率（小数表示）
vols = np.array([0.187, 0.243, 0.312])

# 相关系数
corr_12 = 0.21
corr_13 = -0.13
corr_23 = 0.37

# ==================== 2. 构造协方差矩阵 ====================
# 相关系数矩阵
corr = np.array([
    [1.0,   corr_12, corr_13],
    [corr_12, 1.0,   corr_23],
    [corr_13, corr_23, 1.0  ]
])

# 协方差矩阵: Σ = diag(σ) @ C @ diag(σ) 等价于 σ_i * σ_j * ρ_ij
cov = np.outer(vols, vols) * corr

# ==================== 3. 求解全局最小方差组合 ====================
# 闭式解: w_mvp = Σ^{-1} @ 1 / (1^T @ Σ^{-1} @ 1)
ones = np.ones(3)
cov_inv = np.linalg.inv(cov)

# 计算未归一化的权重
w_unnormalized = cov_inv @ ones

# 归一化使权重和为1（允许卖空，满仓约束）
w_mvp = w_unnormalized / np.sum(w_unnormalized)

# ==================== 4. 计算组合年化波动率 ====================
# 组合方差: σ_p^2 = w^T @ Σ @ w
var_mvp = w_mvp @ cov @ w_mvp
# 组合年化波动率: σ_p = sqrt(σ_p^2)
vol_mvp = np.sqrt(var_mvp)

# ==================== 5. 按契约输出结果 ====================
result = {
    'mvp_weights': w_mvp.tolist(),  # 转为list方便展示与打印
    'mvp_vol_annual': float(vol_mvp)
}

# 打印结果供课堂投屏查看
print("马科维茨全局最小方差组合计算结果：")
print(f"权重 (资产1, 资产2, 资产3): {result['mvp_weights']}")
print(f"年化波动率: {result['mvp_vol_annual']:.4%}")
