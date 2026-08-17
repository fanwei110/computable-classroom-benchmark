import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

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

# 计算组合的期望收益和波动率
def portfolio_stats(weights, expected_returns, cov_matrix):
    port_return = weights @ expected_returns
    port_vol = np.sqrt(weights @ cov_matrix @ weights.T)
    return port_return, port_vol

# 寻找最小方差组合
def find_min_variance_portfolio(expected_returns, cov_matrix):
    n_assets = len(expected_returns)
    initial_weights = np.ones(n_assets) / n_assets
    bounds = [(None, None) for _ in range(n_assets)]  # 允许卖空
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})  # 满仓

    result = minimize(lambda w: portfolio_stats(w, expected_returns, cov_matrix)[1],
                      initial_weights,
                      method='SLSQP',
                      bounds=bounds,
                      constraints=constraints)
    return result.x

# 寻找给定期望收益下的最小波动率组合
def find_portfolio_for_target_return(target_return, expected_returns, cov_matrix):
    n_assets = len(expected_returns)
    initial_weights = np.ones(n_assets) / n_assets
    bounds = [(None, None) for _ in range(n_assets)]  # 允许卖空
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1},  # 满仓
                   {'type': 'eq', 'fun': lambda w: portfolio_stats(w, expected_returns, cov_matrix)[0] - target_return})

    result = minimize(lambda w: portfolio_stats(w, expected_returns, cov_matrix)[1],
                      initial_weights,
                      method='SLSQP',
                      bounds=bounds,
                      constraints=constraints)
    return result.x

# 生成均值-方差前沿
def generate_efficient_frontier(expected_returns, cov_matrix, n_points=100):
    min_var_weights = find_min_variance_portfolio(expected_returns, cov_matrix)
    min_var_return, min_var_vol = portfolio_stats(min_var_weights, expected_returns, cov_matrix)

    target_returns = np.linspace(min_var_return, 0.2, n_points)
    frontier_vols = []

    for ret in target_returns:
        weights = find_portfolio_for_target_return(ret, expected_returns, cov_matrix)
        _, vol = portfolio_stats(weights, expected_returns, cov_matrix)
        frontier_vols.append(vol)

    return target_returns, frontier_vols, min_var_vol

# 主计算过程
result = {}

# 计算rho=0.45时的最小方差组合波动率
cov_matrix_rho45 = get_covariance_matrix(volatilities[0], volatilities[1], 0.45)
mvp_weights_rho45 = find_min_variance_portfolio(expected_returns, cov_matrix_rho45)
_, mvp_vol_rho45 = portfolio_stats(mvp_weights_rho45, expected_returns, cov_matrix_rho45)
result['mvp_vol_at_rho45'] = mvp_vol_rho45

# 计算rho=0.45时目标收益10%的最小波动率
target_weights_rho45 = find_portfolio_for_target_return(target_return, expected_returns, cov_matrix_rho45)
_, target_vol_rho45 = portfolio_stats(target_weights_rho45, expected_returns, cov_matrix_rho45)
result['frontier_vol_at_target'] = target_vol_rho45

# 绘制图形
plt.figure(figsize=(10, 6))

for rho in correlations:
    cov_matrix = get_covariance_matrix(volatilities[0], volatilities[1], rho)
    target_returns, frontier_vols, min_var_vol = generate_efficient_frontier(expected_returns, cov_matrix)

    # 绘制前沿曲线
    plt.plot(frontier_vols, target_returns, label=f'ρ = {rho}')

    # 标记最小方差组合点
    min_var_weights = find_min_variance_portfolio(expected_returns, cov_matrix)
    min_var_return, _ = portfolio_stats(min_var_weights, expected_returns, cov_matrix)
    plt.scatter(min_var_vol, min_var_return, color='red', zorder=5)
    plt.text(min_var_vol, min_var_return, f'MVP (ρ={rho})', fontsize=9,
             verticalalignment='bottom', horizontalalignment='right')

# 标记单个资产点
plt.scatter(volatilities[0], expected_returns[0], color='black', marker='o', label='Asset 1')
plt.scatter(volatilities[1], expected_returns[1], color='black', marker='^', label='Asset 2')

plt.title('Mean-Variance Efficient Frontier with Different Correlations')
plt.xlabel('Annualized Volatility')
plt.ylabel('Expected Annual Return')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = figure_path

# 关闭图形以释放内存
plt.close()

# 输出结果
print(result)
