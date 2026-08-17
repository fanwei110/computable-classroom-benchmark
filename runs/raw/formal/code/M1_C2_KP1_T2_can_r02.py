import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 给定数据
mu = np.array([0.071, 0.124])  # 期望收益
vol = np.array([0.163, 0.289])  # 波动率
target_return = 0.10  # 目标收益率

# 相关系数列表
correlations = [0.15, 0.45, 0.75]

# 存储结果的字典
result = {}

# 绘图设置
plt.figure(figsize=(10, 6))

# 对每个相关系数进行处理
for rho in correlations:
    # 构建协方差矩阵
    Sigma = np.array([
        [vol[0]**2, rho * vol[0] * vol[1]],
        [rho * vol[0] * vol[1], vol[1]**2]
    ])

    # 定义组合方差函数
    def portfolio_variance(w):
        return w.T @ Sigma @ w

    # 定义约束条件：满仓（权重之和为1）
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

    # 找到最小方差组合
    initial_guess = np.array([0.5, 0.5])
    res_mvp = minimize(portfolio_variance, initial_guess, constraints=constraints)
    w_mvp = res_mvp.x
    mu_mvp = w_mvp @ mu
    vol_mvp = np.sqrt(portfolio_variance(w_mvp))

    # 扫描不同权重组合，绘制有效前沿
    n_points = 100
    w1_range = np.linspace(-1, 2, n_points)  # 允许卖空
    frontier_vol = []
    frontier_mu = []

    for w1 in w1_range:
        w = np.array([w1, 1 - w1])
        port_vol = np.sqrt(portfolio_variance(w))
        port_mu = w @ mu
        frontier_vol.append(port_vol)
        frontier_mu.append(port_mu)

    # 绘制有效前沿
    plt.plot(frontier_vol, frontier_mu, label=f'ρ = {rho}')

    # 标记最小方差组合
    plt.scatter(vol_mvp, mu_mvp, color='red', zorder=5)
    plt.text(vol_mvp, mu_mvp, 'MVP', fontsize=9, ha='right')

    # 计算相关系数为0.45时的特定结果
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = vol_mvp

        # 找到目标收益10%下的最小波动率
        def objective(w):
            return w.T @ Sigma @ w

        constraints_target = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ mu - target_return}
        )

        res_target = minimize(objective, initial_guess, constraints=constraints_target)
        w_target = res_target.x
        vol_target = np.sqrt(objective(w_target))
        result['frontier_vol_at_target'] = vol_target

# 图形设置
plt.title('Mean-Variance Frontier for Two Assets')
plt.xlabel('Annualized Volatility')
plt.ylabel('Expected Annual Return')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'mean_variance_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = figure_path

# 输出结果
print(result)
