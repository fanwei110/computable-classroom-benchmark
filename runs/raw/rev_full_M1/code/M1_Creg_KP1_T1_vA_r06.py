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

# 初始猜测（等权重）
initial_weights = np.array([1/3, 1/3, 1/3])

# 优化求解最小方差组合
result_optimization = minimize(
    fun=portfolio_variance,
    x0=initial_weights,
    args=(cov_matrix,),
    constraints=constraints,
    bounds=[(None, None) for _ in range(3)]  # 允许卖空
)

# 提取结果
mvp_weights = result_optimization.x
mvp_variance = result_optimization.fun
mvp_vol_annual = np.sqrt(mvp_variance)

# 存储结果
result = {
    'mvp_weights': mvp_weights,
    'mvp_vol_annual': mvp_vol_annual
}

# 输出结果（可选，用于验证）
print("Global Minimum Variance Portfolio:")
print(f"Weights: {mvp_weights}")
print(f"Annualized Volatility: {mvp_vol_annual:.4f}")
