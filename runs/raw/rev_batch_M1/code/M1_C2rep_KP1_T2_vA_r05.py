import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 给定数据
mu = np.array([0.071, 0.124])  # 期望收益
sigma = np.array([0.163, 0.289])  # 波动率
target_return = 0.10  # 目标收益率

# 相关系数列表
correlations = [0.15, 0.45, 0.75]

# 存储结果的字典
result = {}

# 1. 构造协方差矩阵并绘制前沿
plt.figure(figsize=(10, 6))

for rho in correlations:
    # 构造协方差矩阵
    cov_matrix = np.array([
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [rho * sigma[0] * sigma[1], sigma[1]**2]
    ])

    # 定义组合方差函数
    def portfolio_variance(w, cov_matrix):
        return w.T @ cov_matrix @ w

    # 定义约束条件：满仓（权重之和为1）
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

    # 找到最小方差组合
    initial_guess = np.array([0.5, 0.5])
    res_mvp = minimize(portfolio_variance, initial_guess, args=(cov_matrix,), constraints=constraints)
    w_mvp = res_mvp.x
    mu_mvp = w_mvp @ mu
    vol_mvp = np.sqrt(portfolio_variance(w_mvp, cov_matrix))

    # 如果是rho=0.45，记录最小方差组合的波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = vol_mvp

    # 生成有效前沿
    target_returns = np.linspace(mu_mvp, max(mu), 50)
    frontier_vols = []

    for r in target_returns:
        # 约束条件：期望收益等于r，权重之和为1
        constraints = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ mu - r}
        )
        res = minimize(portfolio_variance, initial_guess, args=(cov_matrix,), constraints=constraints)
        frontier_vols.append(np.sqrt(res.fun))

    # 绘制前沿
    plt.plot(frontier_vols, target_returns, label=f'ρ = {rho}')

    # 标记最小方差组合
    plt.scatter(vol_mvp, mu_mvp, color='red', zorder=5)
    plt.text(vol_mvp, mu_mvp, 'MVP', fontsize=9, verticalalignment='bottom')

    # 如果是rho=0.45，计算目标收益10%下的最小波动率
    if rho == 0.45:
        constraints = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ mu - target_return}
        )
        res_target = minimize(portfolio_variance, initial_guess, args=(cov_matrix,), constraints=constraints)
        result['frontier_vol_at_target'] = np.sqrt(res_target.fun)

# 图形设置
plt.title('Mean-Variance Frontier for Different Correlations')
plt.xlabel('Annualized Volatility')
plt.ylabel('Expected Annual Return')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = figure_path

# 显示图形（可选，根据实际需求决定是否显示）
# plt.show()
