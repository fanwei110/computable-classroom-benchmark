import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 资产参数
mu = np.array([0.071, 0.124])  # 期望收益
vol = np.array([0.163, 0.289])  # 波动率
correlations = [0.15, 0.45, 0.75]  # 相关系数列表

# 存储结果的字典
result = {
    'mvp_vol_at_rho45': None,
    'frontier_vol_at_target': None,
    'figure_path': 'efficient_frontier.png'
}

# 1. 构造协方差矩阵并绘制有效前沿
plt.figure(figsize=(10, 6))

for rho in correlations:
    # 构造协方差矩阵
    Sigma = np.array([
        [vol[0]**2, rho * vol[0] * vol[1]],
        [rho * vol[0] * vol[1], vol[1]**2]
    ])

    # 定义组合方差函数
    def portfolio_variance(w):
        return w.T @ Sigma @ w

    # 定义约束条件：满仓（权重之和为1）
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

    # 扫描不同的目标收益，计算最小方差组合
    target_returns = np.linspace(mu.min(), mu.max(), 100)
    frontier_vols = []

    for r in target_returns:
        # 约束：收益等于目标收益
        constraints_with_return = (
            {'type': 'eq', 'fun': lambda w: np.sum(w * mu) - r},
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
        )
        # 初始猜测
        w0 = np.array([0.5, 0.5])
        # 优化
        res = minimize(portfolio_variance, w0, constraints=constraints_with_return)
        frontier_vols.append(np.sqrt(res.fun))

    # 绘制有效前沿
    plt.plot(frontier_vols, target_returns, label=f'ρ = {rho}')

    # 计算最小方差组合（无收益约束）
    res_mvp = minimize(portfolio_variance, w0, constraints=constraints)
    mvp_vol = np.sqrt(res_mvp.fun)
    mvp_return = res_mvp.x @ mu
    plt.scatter(mvp_vol, mvp_return, color='red', zorder=5)
    plt.text(mvp_vol, mvp_return, 'MVP', fontsize=9, verticalalignment='bottom')

    # 记录ρ=0.45时的最小方差组合波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = mvp_vol

# 2. 计算ρ=0.45时目标收益10%的最小波动率
rho = 0.45
Sigma = np.array([
    [vol[0]**2, rho * vol[0] * vol[1]],
    [rho * vol[0] * vol[1], vol[1]**2]
])

# 约束：收益等于10%，满仓
constraints_target = (
    {'type': 'eq', 'fun': lambda w: np.sum(w * mu) - 0.10},
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
)
w0 = np.array([0.5, 0.5])
res_target = minimize(portfolio_variance, w0, constraints=constraints_target)
result['frontier_vol_at_target'] = np.sqrt(res_target.fun)

# 图形设置
plt.title('Efficient Frontier for Two Assets with Different Correlations')
plt.xlabel('Portfolio Volatility (Annualized)')
plt.ylabel('Portfolio Expected Return (Annualized)')
plt.legend()
plt.grid(True)

# 保存图形
plt.savefig(result['figure_path'])
plt.close()

# 输出结果
print(result)
