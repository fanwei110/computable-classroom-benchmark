import numpy as np
import pandas as pd
from scipy.optimize import minimize

# 风险资产的年化波动率
vol_1 = 0.187
vol_2 = 0.243
vol_3 = 0.312

# 相关系数矩阵
corr_matrix = np.array([
    [1.0,   0.21,  -0.13],
    [0.21,  1.0,    0.37],
    [-0.13, 0.37,   1.0]
])

# 协方差矩阵
sigma = np.array([
    [vol_1**2,                      vol_1 * vol_2 * corr_matrix[0,1], vol_1 * vol_3 * corr_matrix[0,2]],
    [vol_2 * vol_1 * corr_matrix[1,0], vol_2**2,                      vol_2 * vol_3 * corr_matrix[1,2]],
    [vol_3 * vol_1 * corr_matrix[2,0], vol_3 * vol_2 * corr_matrix[2,1], vol_3**2]
])

# 定义目标函数：组合方差
def portfolio_variance(weights):
    return weights @ sigma @ weights

# 约束条件：权重之和等于1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

# 初始权重（等权重）
initial_weights = np.array([1/3, 1/3, 1/3])

# 允许卖空，无上下界限制
bounds = None

# 优化求解
result_optimization = minimize(
    portfolio_variance,
    initial_weights,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints,
    options={'ftol': 1e-12, 'maxiter': 10000}
)

# 全局最小方差组合权重
mvp_weights = result_optimization.x

# 全局最小方差组合的年化波动率
mvp_variance = portfolio_variance(mvp_weights)
mvp_vol_annual = np.sqrt(mvp_variance)

# 将结果存储到字典
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 输出结果
print("全局最小方差组合权重：")
print(f"资产1: {mvp_weights[0]:.6f}")
print(f"资产2: {mvp_weights[1]:.6f}")
print(f"资产3: {mvp_weights[2]:.6f}")
print(f"\n年化波动率: {mvp_vol_annual:.6f} ({mvp_vol_annual*100:.4f}%)")
