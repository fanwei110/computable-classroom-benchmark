import numpy as np
from scipy.optimize import minimize

# 1. 构造协方差矩阵
vols = np.array([0.187, 0.243, 0.312])  # 年化波动率
corr_matrix = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 协方差矩阵 = 波动率向量外积 * 相关系数矩阵
cov_matrix = np.outer(vols, vols) * corr_matrix

# 2. 求最小方差组合权重（满仓约束，允许做空）
n_assets = len(vols)
# 目标函数：组合方差 w'Σw
def portfolio_variance(weights, cov_matrix):
    return weights.T @ cov_matrix @ weights

# 约束：权重和为1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
# 初始猜测：等权重
initial_weights = np.ones(n_assets) / n_assets
# 边界：允许做空（无限制）
bounds = tuple((None, None) for _ in range(n_assets))

# 优化求解
result_optimization = minimize(
    portfolio_variance,
    initial_weights,
    args=(cov_matrix,),
    bounds=bounds,
    constraints=constraints
)

mvp_weights = result_optimization.x
mvp_weights = mvp_weights / np.sum(mvp_weights)  # 确保归一化（理论上优化结果已满足，但数值稳健性考虑）

# 3. 计算组合波动率
mvp_vol = np.sqrt(portfolio_variance(mvp_weights, cov_matrix))
mvp_vol_annual = mvp_vol  # 年化波动率（输入即为年化）

# 4. 输出结果
result = {
    'mvp_weights': mvp_weights.tolist(),
    'mvp_vol_annual': float(mvp_vol_annual)
}

print(result)
