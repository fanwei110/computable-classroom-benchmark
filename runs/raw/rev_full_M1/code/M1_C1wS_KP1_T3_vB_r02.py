import numpy as np

# 1. 确定权重对应方式：60% 对应 A，40% 对应 B
weights = np.array([0.6, 0.4])

# 2. 定义单个资产的波动率（年化）
vol_A = 0.184
vol_B = 0.297

# 3. 构造相关系数为0.3和0.8的协方差矩阵
# 协方差矩阵公式：Σ = [[σ_A², ρ*σ_A*σ_B], [ρ*σ_A*σ_B, σ_B²]]
cov_before = np.array([
    [vol_A**2, 0.3 * vol_A * vol_B],
    [0.3 * vol_A * vol_B, vol_B**2]
])

cov_after = np.array([
    [vol_A**2, 0.8 * vol_A * vol_B],
    [0.8 * vol_A * vol_B, vol_B**2]
])

# 4. 计算组合波动率（年化）：sqrt(w'Σw)
portfolio_vol_before = np.sqrt(weights.T @ cov_before @ weights)
portfolio_vol_after = np.sqrt(weights.T @ cov_after @ weights)

# 5. 存储结果
result = {
    'vol_before_annual': portfolio_vol_before,
    'vol_after_annual': portfolio_vol_after
}

# 打印结果以验证（非必须，但便于课堂展示）
print("60/40组合波动率（相关系数0.3）：{:.4f} 或 {:.2%}".format(
    result['vol_before_annual'], result['vol_before_annual']))
print("60/40组合波动率（相关系数0.8）：{:.4f} 或 {:.2%}".format(
    result['vol_after_annual'], result['vol_after_annual']))
