import numpy as np
from scipy.optimize import minimize

# 1. 构造协方差矩阵
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr_matrix = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 协方差矩阵 = 波动率矩阵 @ 相关系数矩阵 @ 波动率矩阵
vol_matrix = np.diag(vols)
cov_matrix = vol_matrix @ corr_matrix @ vol_matrix

# 2. 求最小方差组合权重（满仓约束）
n_assets = len(vols)
initial_weights = np.ones(n_assets) / n_assets  # 初始猜测

# 定义目标函数（组合方差）
def portfolio_variance(weights, cov_matrix):
    return weights.T @ cov_matrix @ weights

# 约束条件：权重之和为1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

# 优化求解
result_optimization = minimize(
    portfolio_variance,
    initial_weights,
    args=(cov_matrix,),
    constraints=constraints,
    bounds=[(None, None) for _ in range(n_assets)]  # 允许卖空
)

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
