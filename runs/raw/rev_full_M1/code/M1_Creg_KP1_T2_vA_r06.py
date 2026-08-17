import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 设定参数
mu = np.array([0.071, 0.124])  # 期望收益
sigma = np.array([0.163, 0.289])  # 波动率
rho_values = [0.15, 0.45, 0.75]  # 相关系数列表
target_return = 0.10  # 目标收益率

# 计算协方差矩阵
def get_cov_matrix(sigma, rho):
    cov = np.array([
        [sigma[0]**2, sigma[0] * sigma[1] * rho],
        [sigma[0] * sigma[1] * rho, sigma[1]**2]
    ])
    return cov

# 计算组合的期望收益和波动率
def portfolio_stats(weights, mu, cov):
    port_return = weights @ mu
    port_vol = np.sqrt(weights @ cov @ weights.T)
    return port_return, port_vol

# 寻找最小方差组合
def find_mvp(cov):
    n = len(cov)
    def objective(weights):
        return weights @ cov @ weights.T
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = tuple((-np.inf, np.inf) for _ in range(n))
    result = minimize(objective, x0=np.ones(n)/n, bounds=bounds, constraints=constraints)
    return result.x

# 寻找给定收益下的最小波动率组合
def find_min_vol_for_return(target_return, mu, cov):
    n = len(mu)
    def objective(weights):
        return weights @ cov @ weights.T
    constraints = (
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        {'type': 'eq', 'fun': lambda w: w @ mu - target_return}
    )
    bounds = tuple((-np.inf, np.inf) for _ in range(n))
    result = minimize(objective, x0=np.ones(n)/n, bounds=bounds, constraints=constraints)
    return result.x

# 生成有效前沿
def generate_efficient_frontier(mu, cov, n_points=100):
    mvp_weights = find_mvp(cov)
    mvp_return, mvp_vol = portfolio_stats(mvp_weights, mu, cov)

    target_returns = np.linspace(mvp_return, np.max(mu) * 1.1, n_points)
    frontier_vols = []

    for ret in target_returns:
        weights = find_min_vol_for_return(ret, mu, cov)
        _, vol = portfolio_stats(weights, mu, cov)
        frontier_vols.append(vol)

    return target_returns, frontier_vols, mvp_return, mvp_vol

# 主计算过程
result = {}

# 计算rho=0.45时的特定值
rho_45 = 0.45
cov_45 = get_cov_matrix(sigma, rho_45)
mvp_weights_45 = find_mvp(cov_45)
_, mvp_vol_45 = portfolio_stats(mvp_weights_45, mu, cov_45)
result['mvp_vol_at_rho45'] = float(mvp_vol_45)

min_vol_weights_45 = find_min_vol_for_return(target_return, mu, cov_45)
_, min_vol_45 = portfolio_stats(min_vol_weights_45, mu, cov_45)
result['frontier_vol_at_target'] = float(min_vol_45)

# 绘制有效前沿
plt.figure(figsize=(10, 6))

for rho in rho_values:
    cov = get_cov_matrix(sigma, rho)
    target_returns, frontier_vols, mvp_return, mvp_vol = generate_efficient_frontier(mu, cov)

    plt.plot(frontier_vols, target_returns, label=f'ρ = {rho}')
    plt.scatter(mvp_vol, mvp_return, color='red', zorder=5)
    plt.text(mvp_vol, mvp_return, f'MVP (ρ={rho})', fontsize=9,
             verticalalignment='bottom', horizontalalignment='right')

plt.title('Mean-Variance Efficient Frontier with Different Correlations')
plt.xlabel('Annualized Volatility')
plt.ylabel('Expected Annual Return')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

result['figure_path'] = figure_path

# 输出结果
print(result)
