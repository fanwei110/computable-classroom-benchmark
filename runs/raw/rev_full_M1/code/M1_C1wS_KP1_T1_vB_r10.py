import numpy as np
from scipy.optimize import minimize

# 给定数据
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr_12 = 0.21
corr_13 = -0.13
corr_23 = 0.37

# 1. 构造协方差矩阵
cov_matrix = np.zeros((3, 3))
# 对角线元素为方差
cov_matrix[0, 0] = vols[0] ** 2
cov_matrix[1, 1] = vols[1] ** 2
cov_matrix[2, 2] = vols[2] ** 2
# 非对角线元素为协方差
cov_matrix[0, 1] = corr_12 * vols[0] * vols[1]
cov_matrix[1, 0] = cov_matrix[0, 1]
cov_matrix[0, 2] = corr_13 * vols[0] * vols[2]
cov_matrix[2, 0] = cov_matrix[0, 2]
cov_matrix[1, 2] = corr_23 * vols[1] * vols[2]
cov_matrix[2, 1] = cov_matrix[1, 2]

# 2. 求最小方差组合权重（满仓约束）
def portfolio_variance(weights, cov_matrix):
    return weights.T @ cov_matrix @ weights

# 初始猜测权重
initial_weights = np.array([1/3, 1/3, 1/3])
# 约束条件：权重之和为1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
# 边界条件：允许做空（无限制）
bounds = ((-np.inf, np.inf), (-np.inf, np.inf), (-np.inf, np.inf))

# 优化求解
result_optimization = minimize(portfolio_variance,
                              initial_weights,
                              args=(cov_matrix,),
                              method='SLSQP',
                              bounds=bounds,
                              constraints=constraints)

mvp_weights = result_optimization.x

# 3. 计算组合波动率
mvp_variance = portfolio_variance(mvp_weights, cov_matrix)
mvp_vol_annual = np.sqrt(mvp_variance)

# 4. 输出结果
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol_annual)
}

print(result)
