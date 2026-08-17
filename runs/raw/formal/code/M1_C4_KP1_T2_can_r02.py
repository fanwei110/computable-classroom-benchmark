import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 给定数据
mu = np.array([0.071, 0.124])  # 期望收益率
vol = np.array([0.163, 0.289])  # 波动率
target_return = 0.10  # 目标收益率

# 相关系数列表
correlations = [0.15, 0.45, 0.75]

# 存储结果的字典
result = {}

# 创建图形
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

    # 为了绘制有效前沿，我们需要在不同的目标收益下找到最小方差组合
    # 定义目标收益范围
    min_mu = min(mu)
    max_mu = max(mu)
    target_mus = np.linspace(min_mu, max_mu, 100)

    # 存储前沿上的波动率
    frontier_vols = []

    for target_mu in target_mus:
        # 定义约束条件：满仓且期望收益等于目标收益
        constraints = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ mu - target_mu}
        )
        res = minimize(portfolio_variance, initial_guess, constraints=constraints)
        if res.success:
            frontier_vols.append(np.sqrt(res.fun))
        else:
            frontier_vols.append(np.nan)

    # 绘制前沿
    plt.plot(frontier_vols, target_mus, label=f'ρ={rho}')

    # 标记最小方差组合
    plt.scatter(vol_mvp, mu_mvp, color='red', zorder=5)
    plt.text(vol_mvp, mu_mvp, 'MVP', fontsize=9, verticalalignment='bottom')

    # 计算相关系数为0.45时的特定值
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = float(vol_mvp)

        # 计算目标收益10%下的最小波动率
        constraints = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ mu - target_return}
        )
        res_target = minimize(portfolio_variance, initial_guess, constraints=constraints)
        if res_target.success:
            result['frontier_vol_at_target'] = float(np.sqrt(res_target.fun))
        else:
            result['frontier_vol_at_target'] = np.nan

# 设置图形属性
plt.xlabel('波动率 (年化)')
plt.ylabel('期望收益 (年化)')
plt.title('两资产均值-方差有效前沿')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = figure_path

# 显示图形（可选，在课堂上可能不需要）
# plt.show()

# 输出结果
print(result)
