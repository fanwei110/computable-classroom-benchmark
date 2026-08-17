import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 给定数据
mu = np.array([0.071, 0.124])  # 期望收益
vol = np.array([0.163, 0.289])  # 波动率
corr_list = [0.15, 0.45, 0.75]  # 相关系数列表
target_return = 0.10  # 目标收益率

# 结果字典
result = {}

# 1. 构造协方差矩阵并绘制前沿
plt.figure(figsize=(10, 6))

for rho in corr_list:
    # 构造协方差矩阵
    Sigma = np.array([
        [vol[0]**2, rho * vol[0] * vol[1]],
        [rho * vol[0] * vol[1], vol[1]**2]
    ])

    # 定义组合方差函数
    def portfolio_variance(w, Sigma):
        return w.T @ Sigma @ w

    # 定义约束条件：满仓（w1 + w2 = 1）
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = [(-1, 1), (-1, 1)]  # 允许卖空

    # 找到最小方差组合
    res_mvp = minimize(portfolio_variance, x0=[0.5, 0.5], args=(Sigma,),
                       constraints=constraints, bounds=bounds)
    w_mvp = res_mvp.x
    mu_mvp = w_mvp @ mu
    vol_mvp = np.sqrt(portfolio_variance(w_mvp, Sigma))

    # 生成前沿曲线
    target_returns = np.linspace(mu.min(), mu.max(), 100)
    frontier_vols = []

    for r in target_returns:
        constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
                       {'type': 'eq', 'fun': lambda w: w @ mu - r})
        res = minimize(portfolio_variance, x0=[0.5, 0.5], args=(Sigma,),
                       constraints=constraints, bounds=bounds)
        frontier_vols.append(np.sqrt(res.fun))

    # 绘制前沿曲线
    plt.plot(frontier_vols, target_returns, label=f'ρ={rho}')

    # 标记最小方差组合
    plt.scatter(vol_mvp, mu_mvp, color='red', zorder=5)
    plt.text(vol_mvp, mu_mvp, 'MVP', fontsize=9, ha='right')

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

# 2. 计算相关系数为0.45时的特定值
rho_45 = 0.45
Sigma_45 = np.array([
    [vol[0]**2, rho_45 * vol[0] * vol[1]],
    [rho_45 * vol[0] * vol[1], vol[1]**2]
])

# 最小方差组合
res_mvp_45 = minimize(portfolio_variance, x0=[0.5, 0.5], args=(Sigma_45,),
                      constraints=constraints, bounds=bounds)
w_mvp_45 = res_mvp_45.x
vol_mvp_45 = np.sqrt(portfolio_variance(w_mvp_45, Sigma_45))
result['mvp_vol_at_rho45'] = vol_mvp_45

# 目标收益10%下的最小波动率
constraints_target = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
                      {'type': 'eq', 'fun': lambda w: w @ mu - target_return})
res_target = minimize(portfolio_variance, x0=[0.5, 0.5], args=(Sigma_45,),
                      constraints=constraints_target, bounds=bounds)
vol_target = np.sqrt(res_target.fun)
result['frontier_vol_at_target'] = vol_target

# 输出结果
print(result)
