import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 定义风险资产参数
mu = np.array([0.071, 0.124])  # 期望年收益
sigma = np.array([0.163, 0.289])  # 年化波动率
correlations = [0.15, 0.45, 0.75]  # 相关系数列表

# 计算协方差矩阵
def get_cov_matrix(sigma1, sigma2, rho):
    cov = rho * sigma1 * sigma2
    return np.array([[sigma1**2, cov], [cov, sigma2**2]])

# 计算组合的期望收益和波动率
def portfolio_stats(weights, mu, cov):
    port_mu = weights @ mu
    port_vol = np.sqrt(weights @ cov @ weights.T)
    return port_mu, port_vol

# 找到最小方差组合
def find_mvp(mu, cov):
    n = len(mu)
    # 目标函数：组合方差
    def objective(weights):
        return weights @ cov @ weights.T

    # 约束条件：权重之和为1
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = tuple((-np.inf, np.inf) for _ in range(n))  # 允许卖空

    # 初始猜测
    init_guess = np.array([0.5, 0.5])

    # 优化
    res = minimize(objective, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    return res.x

# 生成均值-方差前沿
def generate_frontier(mu, cov, n_points=100):
    mvp_weights = find_mvp(mu, cov)
    mvp_mu, mvp_vol = portfolio_stats(mvp_weights, mu, cov)

    # 生成目标收益率范围
    target_mus = np.linspace(mvp_mu, max(mu), n_points)

    frontier_vols = []
    for target_mu in target_mus:
        # 目标函数：组合方差
        def objective(weights):
            return weights @ cov @ weights.T

        # 约束条件：权重之和为1，期望收益等于目标收益
        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
                       {'type': 'eq', 'fun': lambda w: w @ mu - target_mu})
        bounds = tuple((-np.inf, np.inf) for _ in range(len(mu)))  # 允许卖空

        # 初始猜测
        init_guess = np.array([0.5, 0.5])

        # 优化
        res = minimize(objective, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
        if res.success:
            _, vol = portfolio_stats(res.x, mu, cov)
            frontier_vols.append(vol)

    return target_mus, np.array(frontier_vols), (mvp_mu, mvp_vol)

# 主计算过程
result = {}

# 绘制均值-方差前沿
plt.figure(figsize=(10, 6))

for rho in correlations:
    cov = get_cov_matrix(sigma[0], sigma[1], rho)
    target_mus, frontier_vols, (mvp_mu, mvp_vol) = generate_frontier(mu, cov)

    # 绘制前沿曲线
    plt.plot(frontier_vols, target_mus, label=f'ρ = {rho}')

    # 标记最小方差组合
    plt.scatter(mvp_vol, mvp_mu, color='red', zorder=5)
    plt.text(mvp_vol, mvp_mu, f'MVP (ρ={rho})', fontsize=9,
             verticalalignment='bottom', horizontalalignment='right')

    # 记录rho=0.45时的MVP波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = mvp_vol

# 计算rho=0.45时目标收益10%的最小波动率
rho_45 = 0.45
cov_45 = get_cov_matrix(sigma[0], sigma[1], rho_45)
target_return = 0.10

def objective(weights):
    return weights @ cov_45 @ weights.T

constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
               {'type': 'eq', 'fun': lambda w: w @ mu - target_return})
bounds = tuple((-np.inf, np.inf) for _ in range(len(mu)))

init_guess = np.array([0.5, 0.5])
res = minimize(objective, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
if res.success:
    _, min_vol = portfolio_stats(res.x, mu, cov_45)
    result['frontier_vol_at_target'] = min_vol

# 图形设置
plt.title('Mean-Variance Frontier with Different Correlations')
plt.xlabel('Annualized Volatility')
plt.ylabel('Expected Annual Return')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = figure_path

# 关闭图形以释放内存
plt.close()

# 输出结果
print(result)
