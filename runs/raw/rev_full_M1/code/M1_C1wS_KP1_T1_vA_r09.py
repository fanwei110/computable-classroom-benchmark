import numpy as np
from scipy.optimize import minimize

# 1. 构造协方差矩阵
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr_matrix = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 协方差矩阵 = 波动率对角阵 @ 相关系数矩阵 @ 波动率对角阵
cov_matrix = np.diag(vols) @ corr_matrix @ np.diag(vols)

# 2. 求最小方差组合权重（满仓约束）
n_assets = len(vols)
# 目标函数：组合方差 w'Σw
def portfolio_variance(weights, cov_matrix):
    return weights.T @ cov_matrix @ weights

# 约束：权重之和为1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
# 初始猜测：等权重
initial_guess = np.ones(n_assets) / n_assets
# 边界：允许卖空（无限制）
bounds = tuple((None, None) for _ in range(n_assets))

# 优化求解
result_optim = minimize(
    portfolio_variance,
    initial_guess,
    args=(cov_matrix,),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

mvp_weights = result_optim.x

# 3. 计算组合波动率
mvp_variance = portfolio_variance(mvp_weights, cov_matrix)
mvp_vol_annual = np.sqrt(mvp_variance)

# 4. 填充结果字典
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol_annual)
}

print(result)
