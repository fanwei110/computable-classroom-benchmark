import numpy as np

# 年化波动率
sigma = np.array([0.187, 0.243, 0.312])

# 相关系数矩阵
corr = np.array([
    [1.00,  0.21, -0.13],
    [0.21,  1.00,  0.37],
    [-0.13, 0.37,  1.00]
])

# 1. 构造协方差矩阵 Σ = diag(sigma) @ corr @ diag(sigma)
cov = np.diag(sigma) @ corr @ np.diag(sigma)

# 2. 全局最小方差组合权重（允许卖空，满仓）
# w = Σ^{-1} 1 / (1' Σ^{-1} 1)
inv_cov = np.linalg.inv(cov)
ones = np.ones(len(sigma))
w_mvp = inv_cov @ ones / (ones @ inv_cov @ ones)

# 3. 组合年化波动率
var_mvp = w_mvp @ cov @ w_mvp
vol_mvp = np.sqrt(var_mvp)

# 4. 按要求键名填充结果
result = {
    'mvp_weights': list(w_mvp),  # 转为普通列表，确保可序列化
    'mvp_vol_annual': float(vol_mvp)
}

# 展示结果（会被教师投屏看到）
print("全局最小方差组合计算结果：")
print("权重：", result['mvp_weights'])
print(f"年化波动率：{result['mvp_vol_annual']:.4f}")
