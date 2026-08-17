import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import os

# 设定参数
expected_returns = np.array([0.071, 0.124])
volatilities = np.array([0.163, 0.289])
correlations = [0.15, 0.45, 0.75]
target_return = 0.10

# 计算协方差矩阵
def get_covariance_matrix(vol1, vol2, rho):
    cov = rho * vol1 * vol2
    return np.array([[vol1**2, cov], [cov, vol2**2]])

# 最小化方差的优化函数
def portfolio_variance(weights, cov_matrix):
    return weights.T @ cov_matrix @ weights

# 约束条件：权重之和为1
constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

# 生成均值-方差前沿
def generate_frontier(expected_returns, cov_matrix, n_points=100):
    min_ret = expected_returns.min()
    max_ret = expected_returns.max()
    target_returns = np.linspace(min_ret, max_ret, n_points)

    frontier_vols = []
    for ret in target_returns:
        constraints_with_ret = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ expected_returns - ret}
        )
        result = minimize(portfolio_variance,
                         x0=np.array([0.5, 0.5]),
                         args=(cov_matrix,),
                         constraints=constraints_with_ret,
                         bounds=((-np.inf, np.inf), (-np.inf, np.inf)))
        frontier_vols.append(np.sqrt(result.fun))

    return target_returns, np.array(frontier_vols)

# 找到最小方差组合
def find_mvp(cov_matrix):
    result = minimize(portfolio_variance,
                     x0=np.array([0.5, 0.5]),
                     args=(cov_matrix,),
                     constraints=constraints,
                     bounds=((-np.inf, np.inf), (-np.inf, np.inf)))
    mvp_vol = np.sqrt(result.fun)
    mvp_ret = result.x @ expected_returns
    return mvp_ret, mvp_vol

# 主计算过程
result = {}

# 计算相关系数为0.45时的特定值
rho_45 = 0.45
cov_matrix_45 = get_covariance_matrix(volatilities[0], volatilities[1], rho_45)

# 最小方差组合的波动率
mvp_ret_45, mvp_vol_45 = find_mvp(cov_matrix_45)
result['mvp_vol_at_rho45'] = float(mvp_vol_45)

# 目标收益10%时的最小波动率
constraints_with_target = (
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
    {'type': 'eq', 'fun': lambda w: w @ expected_returns - target_return}
)
target_result = minimize(portfolio_variance,
                        x0=np.array([0.5, 0.5]),
                        args=(cov_matrix_45,),
                        constraints=constraints_with_target,
                        bounds=((-np.inf, np.inf), (-np.inf, np.inf)))
result['frontier_vol_at_target'] = float(np.sqrt(target_result.fun))

# 绘制图形
plt.figure(figsize=(10, 6))

for rho in correlations:
    cov_matrix = get_covariance_matrix(volatilities[0], volatilities[1], rho)
    frontier_rets, frontier_vols = generate_frontier(expected_returns, cov_matrix)
    mvp_ret, mvp_vol = find_mvp(cov_matrix)

    plt.plot(frontier_vols, frontier_rets, label=f'ρ = {rho}')
    plt.scatter(mvp_vol, mvp_ret, color='red', zorder=5)
    plt.text(mvp_vol, mvp_ret, f'MVP (ρ={rho})', fontsize=9,
             verticalalignment='bottom', horizontalalignment='right')

plt.xlabel('Annualized Volatility')
plt.ylabel('Expected Annual Return')
plt.title('Mean-Variance Frontier for Different Correlations')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path)
plt.close()

result['figure_path'] = os.path.abspath(figure_path)

# 输出结果
print(result)
