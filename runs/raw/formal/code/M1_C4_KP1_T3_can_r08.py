import numpy as np

# 给定参数
vol_A = 0.184  # 资产A的年化波动率
vol_B = 0.297  # 资产B的年化波动率
weights = np.array([0.6, 0.4])  # 组合权重：A 60%, B 40%

# 相关系数变化
corr_before = 0.3
corr_after = 0.8

# 构造协方差矩阵
# 协方差矩阵公式：Σ = [[σ_A^2, σ_A * σ_B * ρ], [σ_A * σ_B * ρ, σ_B^2]]
cov_before = np.array([
    [vol_A ** 2, vol_A * vol_B * corr_before],
    [vol_A * vol_B * corr_before, vol_B ** 2]
])

cov_after = np.array([
    [vol_A ** 2, vol_A * vol_B * corr_after],
    [vol_A * vol_B * corr_after, vol_B ** 2]
])

# 计算组合波动率：sqrt(w'Σw)
portfolio_vol_before = np.sqrt(weights.T @ cov_before @ weights)
portfolio_vol_after = np.sqrt(weights.T @ cov_after @ weights)

# 存储结果
result = {
    'vol_before_annual': portfolio_vol_before,
    'vol_after_annual': portfolio_vol_after
}

print(result)
