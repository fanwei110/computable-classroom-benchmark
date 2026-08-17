import numpy as np
from scipy.optimize import minimize

# 1. 构造协方差矩阵
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr_matrix = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 协方差矩阵 = 相关系数矩阵 * 波动率向量外积
cov_matrix = corr_matrix * np.outer(vols, vols)

# 2. 求最小方差组合权重（满仓约束：权重和为1）
def portfolio_variance(weights, cov_matrix):
    return weights.T @ cov_matrix @ weights

# 初始猜测（均匀分配）
initial_weights = np.array([1/3, 1/3, 1/3])

# 约束：权重和为1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

# 允许做空（无边界约束）
bounds = ((None, None), (None, None), (None, None))

# 优化求解
result_optimization = minimize(
    portfolio_variance,
    initial_weights,
    args=(cov_matrix,),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

mvp_weights = result_optimization.x

# 3. 计算组合波动率（年化）
mvp_variance = portfolio_variance(mvp_weights, cov_matrix)
mvp_vol_annual = np.sqrt(mvp_variance)

# 4. 输出结果
result = {
    'mvp_weights': mvp_weights.tolist(),  # 转为列表以确保可序列化
    'mvp_vol_annual': float(mvp_vol_annual)  # 转为Python float
}

print(result)
