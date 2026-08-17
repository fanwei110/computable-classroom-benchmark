import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 给定数据
mu = np.array([0.071, 0.124])  # 期望收益
vol = np.array([0.163, 0.289])  # 波动率
correlations = [0.15, 0.45, 0.75]  # 相关系数
target_return = 0.10  # 目标收益

# 结果字典
result = {}

# 1. 构造协方差矩阵并绘制有效前沿
plt.figure(figsize=(10, 6))

for rho in correlations:
    # 构造协方差矩阵
    Sigma = np.array([
        [vol[0]**2, rho * vol[0] * vol[1]],
        [rho * vol[0] * vol[1], vol[1]**2]
    ])

    # 定义组合方差函数
    def portfolio_variance(w, Sigma):
        return w.T @ Sigma @ w

    # 定义约束条件：满仓 (w1 + w2 = 1)
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

    # 扫描不同的目标收益，计算最小方差组合
    target_returns = np.linspace(min(mu), max(mu), 100)
    frontier_vols = []

    for r in target_returns:
        # 约束：期望收益等于 r
        constraints_with_return = (
            {'type': 'eq', 'fun': lambda w: np.sum(w * mu) - r},
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
        )
        # 初始猜测
        w0 = np.array([0.5, 0.5])
        # 优化
        res = minimize(portfolio_variance, w0, args=(Sigma,), constraints=constraints_with_return)
        frontier_vols.append(np.sqrt(res.fun))

    # 绘制有效前沿
    plt.plot(frontier_vols, target_returns, label=f'ρ = {rho}')

    # 2. 标出最小方差组合 (MVP)
    # 仅满仓约束，无收益约束
    res_mvp = minimize(portfolio_variance, w0, args=(Sigma,), constraints=constraints)
    mvp_vol = np.sqrt(res_mvp.fun)
    mvp_return = res_mvp.x @ mu
    plt.scatter(mvp_vol, mvp_return, color='red', zorder=5)
    plt.text(mvp_vol, mvp_return, 'MVP', fontsize=9, verticalalignment='bottom')

# 图形设置
plt.xlabel('Annualized Volatility')
plt.ylabel('Expected Annual Return')
plt.title('Mean-Variance Frontier for Two Assets')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = figure_path

# 3. 计算相关系数为 0.45 时的两个波动率
rho_45 = 0.45
Sigma_45 = np.array([
    [vol[0]**2, rho_45 * vol[0] * vol[1]],
    [rho_45 * vol[0] * vol[1], vol[1]**2]
])

# 最小方差组合 (MVP)
res_mvp_45 = minimize(portfolio_variance, w0, args=(Sigma_45,), constraints=constraints)
mvp_vol_45 = np.sqrt(res_mvp_45.fun)
result['mvp_vol_at_rho45'] = float(mvp_vol_45)

# 目标收益 10% 下的最小波动率
constraints_with_target = (
    {'type': 'eq', 'fun': lambda w: np.sum(w * mu) - target_return},
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
)
res_target = minimize(portfolio_variance, w0, args=(Sigma_45,), constraints=constraints_with_target)
frontier_vol_target = np.sqrt(res_target.fun)
result['frontier_vol_at_target'] = float(frontier_vol_target)

# 输出结果
print(result)
