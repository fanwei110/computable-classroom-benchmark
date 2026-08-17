import numpy as np

# 1. 参数设定（按约定使用小数表示）
sigma_A = 0.184
sigma_B = 0.297

# 按资产被提及的顺序对应：A占60%，B占40%
w_A = 0.6
w_B = 0.4
w = np.array([w_A, w_B])

# 2. 构造两个相关系数下的协方差矩阵
# 协方差公式：Cov(A, B) = rho * sigma_A * sigma_B

# 相关系数为 0.3 时的协方差矩阵
cov_matrix_before = np.array([
    [sigma_A**2, 0.3 * sigma_A * sigma_B],
    [0.3 * sigma_A * sigma_B, sigma_B**2]
])

# 相关系数为 0.8 时的协方差矩阵
cov_matrix_after = np.array([
    [sigma_A**2, 0.8 * sigma_A * sigma_B],
    [0.8 * sigma_A * sigma_B, sigma_B**2]
])

# 3. 计算两个组合波动率（小数表示）
# 组合方差公式：w'Σw
var_before = w.T @ cov_matrix_before @ w
var_after = w.T @ cov_matrix_after @ w

# 组合波动率（标准差）
vol_before = np.sqrt(var_before)
vol_after = np.sqrt(var_after)

# 4. 填充 result 字典
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}

# 课堂展示输出
print(f"相关系数 0.3 时的组合年化波动率: {result['vol_before_annual']:.4%}")
print(f"相关系数 0.8 时的组合年化波动率: {result['vol_after_annual']:.4%}")
print(f"波动率变化量: {(result['vol_after_annual'] - result['vol_before_annual']):.4%}")
