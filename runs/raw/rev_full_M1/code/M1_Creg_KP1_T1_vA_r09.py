import numpy as np
from scipy.optimize import minimize

# 输入数据
volatilities = np.array([0.187, 0.243, 0.312])  # 年化波动率
correlations = np.array([
    [1.0, 0.21, -0.13],
    [0.21, 1.0, 0.37],
    [-0.13, 0.37, 1.0]
])

# 计算协方差矩阵
cov_matrix = np.outer(volatilities, volatilities) * correlations

# 定义组合方差函数
def portfolio_variance(weights, cov_matrix):
    return weights.T @ cov_matrix @ weights

# 约束条件：权重之和为1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

# 优化求解最小方差组合
initial_weights = np.array([1/3, 1/3, 1/3])  # 初始猜测
bounds = [(-1, 1) for _ in range(len(volatilities))]  # 允许卖空，权重范围[-1,1]

result_optimization = minimize(
    portfolio_variance,
    initial_weights,
    args=(cov_matrix,),
    method='SLSQP',
    bounds=bounds,
    constraints=constraints
)

# 提取结果
mvp_weights = result_optimization.x
mvp_vol_annual = np.sqrt(portfolio_variance(mvp_weights, cov_matrix))

# 存储结果
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 打印结果以验证
print("全局最小方差组合权重:", result['mvp_weights'])
print("全局最小方差组合年化波动率:", result['mvp_vol_annual'])
