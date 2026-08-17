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
    cov_matrix = np.array([[vol1**2, cov], [cov, vol2**2]])
    return cov_matrix

# 最小化方差的优化函数
def portfolio_variance(weights, cov_matrix):
    return weights.T @ cov_matrix @ weights

# 计算均值-方差前沿
def calculate_frontier(expected_returns, cov_matrix):
    n_assets = len(expected_returns)
    constraints = (
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},  # 满仓
    )
    bounds = tuple((None, None) for _ in range(n_assets))  # 允许卖空

    # 计算最小方差组合
    res_mvp = minimize(
        portfolio_variance,
        x0=np.ones(n_assets) / n_assets,
        args=(cov_matrix,),
        constraints=constraints,
        bounds=bounds
    )
    mvp_weights = res_mvp.x
    mvp_return = mvp_weights @ expected_returns
    mvp_vol = np.sqrt(portfolio_variance(mvp_weights, cov_matrix))

    # 计算前沿
    target_returns = np.linspace(mvp_return, 0.2, 100)
    frontier_vols = []
    for r in target_returns:
        constraints_with_return = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ expected_returns - r}
        )
        res = minimize(
            portfolio_variance,
            x0=np.ones(n_assets) / n_assets,
            args=(cov_matrix,),
            constraints=constraints_with_return,
            bounds=bounds
        )
        frontier_vols.append(np.sqrt(res.fun))

    return {
        'mvp_return': mvp_return,
        'mvp_vol': mvp_vol,
        'target_returns': target_returns,
        'frontier_vols': frontier_vols
    }

# 计算目标收益下的最小波动率
def min_vol_at_target(expected_returns, cov_matrix, target_return):
    n_assets = len(expected_returns)
    constraints = (
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        {'type': 'eq', 'fun': lambda w: w @ expected_returns - target_return}
    )
    bounds = tuple((None, None) for _ in range(n_assets))
    res = minimize(
        portfolio_variance,
        x0=np.ones(n_assets) / n_assets,
        args=(cov_matrix,),
        constraints=constraints,
        bounds=bounds
    )
    return np.sqrt(res.fun)

# 主计算
result = {}
rho_45_cov_matrix = get_covariance_matrix(volatilities[0], volatilities[1], 0.45)
rho_45_frontier = calculate_frontier(expected_returns, rho_45_cov_matrix)
result['mvp_vol_at_rho45'] = rho_45_frontier['mvp_vol']
result['frontier_vol_at_target'] = min_vol_at_target(expected_returns, rho_45_cov_matrix, target_return)

# 绘图
plt.figure(figsize=(10, 6))
for rho in correlations:
    cov_matrix = get_covariance_matrix(volatilities[0], volatilities[1], rho)
    frontier = calculate_frontier(expected_returns, cov_matrix)
    plt.plot(frontier['frontier_vols'], frontier['target_returns'], label=f'ρ={rho}')
    plt.scatter(frontier['mvp_vol'], frontier['mvp_return'], color='red', zorder=5)
    plt.text(frontier['mvp_vol'], frontier['mvp_return'], 'MVP', fontsize=9, ha='right')

plt.xlabel('Annualized Volatility')
plt.ylabel('Expected Annual Return')
plt.title('Mean-Variance Frontier for Different Correlations')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path)
plt.close()

result['figure_path'] = os.path.abspath(figure_path)

# 输出结果
print(result)
