import numpy as np

# 给定参数
vol_A = 0.184  # 资产A的年化波动率
vol_B = 0.297  # 资产B的年化波动率
weight_A = 0.6  # 组合中A的权重
weight_B = 0.4  # 组合中B的权重

# 相关系数变化前后的值
corr_before = 0.3
corr_after = 0.8

# 1. 构造协方差矩阵
# 协方差矩阵公式: Σ = [[σ_A², ρ*σ_A*σ_B], [ρ*σ_A*σ_B, σ_B²]]
cov_before = np.array([
    [vol_A ** 2, corr_before * vol_A * vol_B],
    [corr_before * vol_A * vol_B, vol_B ** 2]
])

cov_after = np.array([
    [vol_A ** 2, corr_after * vol_A * vol_B],
    [corr_after * vol_A * vol_B, vol_B ** 2]
])

# 2. 计算组合波动率
# 组合方差 = w'Σw
weights = np.array([weight_A, weight_B])

portfolio_var_before = weights.T @ cov_before @ weights
portfolio_vol_before = np.sqrt(portfolio_var_before)  # 年化波动率

portfolio_var_after = weights.T @ cov_after @ weights
portfolio_vol_after = np.sqrt(portfolio_var_after)  # 年化波动率

# 3. 存储结果
result = {
    'vol_before_annual': portfolio_vol_before,
    'vol_after_annual': portfolio_vol_after
}

print(result)
