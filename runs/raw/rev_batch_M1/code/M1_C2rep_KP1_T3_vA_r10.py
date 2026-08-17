import numpy as np

# 1. 确定权重对应方式：60/40 组合，A 占 60%，B 占 40%
weights = np.array([0.6, 0.4])  # [A, B]

# 2. 资产年化波动率（标准差）
vol_A = 0.184
vol_B = 0.297

# 3. 构造协方差矩阵
# 相关系数 0.3 时的协方差矩阵
corr_before = 0.3
cov_before = np.array([
    [vol_A ** 2, corr_before * vol_A * vol_B],
    [corr_before * vol_A * vol_B, vol_B ** 2]
])

# 相关系数 0.8 时的协方差矩阵
corr_after = 0.8
cov_after = np.array([
    [vol_A ** 2, corr_after * vol_A * vol_B],
    [corr_after * vol_A * vol_B, vol_B ** 2]
])

# 4. 计算组合波动率（年化）
# 组合方差 = w'Σw
var_before = weights.T @ cov_before @ weights
vol_before_annual = np.sqrt(var_before)

var_after = weights.T @ cov_after @ weights
vol_after_annual = np.sqrt(var_after)

# 5. 填充 result 字典
result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}

# 输出结果以供验证（非契约要求，仅方便调试）
print(result)
