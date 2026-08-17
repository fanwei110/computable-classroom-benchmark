import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 资产参数
mu = np.array([0.071, 0.124])          # 期望收益
sigma = np.array([0.163, 0.289])       # 波动率
correlations = [0.15, 0.45, 0.75]      # 相关系数列表

# 存储结果的字典
result = {}

# 1. 构造协方差矩阵并绘制有效前沿
plt.figure(figsize=(10, 6))

for rho in correlations:
    # 构造协方差矩阵
    Sigma = np.array([
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [rho * sigma[0] * sigma[1], sigma[1]**2]
    ])

    # 定义组合方差函数
    def portfolio_variance(w):
        return w.T @ Sigma @ w

    # 定义约束：满仓（权重之和为1）
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})

    # 扫描不同目标收益下的最小方差组合
    target_returns = np.linspace(mu.min(), mu.max(), 100)
    frontier_volatilities = []

    for r in target_returns:
        # 约束：收益等于目标收益
        constraints_with_return = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ mu - r}
        )
        # 初始猜测
        w0 = np.array([0.5, 0.5])
        # 优化
        res = minimize(portfolio_variance, w0, constraints=constraints_with_return)
        frontier_volatilities.append(np.sqrt(res.fun))

    # 绘制有效前沿
    plt.plot(frontier_volatilities, target_returns, label=f'ρ={rho}')

    # 2. 标记最小方差组合（MVP）
    # 仅满仓约束下最小化方差
    res_mvp = minimize(portfolio_variance, w0, constraints=constraints)
    mvp_vol = np.sqrt(res_mvp.fun)
    mvp_ret = res_mvp.x @ mu
    plt.scatter(mvp_vol, mvp_ret, color='red', zorder=5)
    plt.text(mvp_vol, mvp_ret, 'MVP', fontsize=9, ha='right')

    # 存储 ρ=0.45 时的 MVP 波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = mvp_vol

# 3. 计算 ρ=0.45 时目标收益 10% 的最小波动率
rho_45 = 0.45
Sigma_45 = np.array([
    [sigma[0]**2, rho_45 * sigma[0] * sigma[1]],
    [rho_45 * sigma[0] * sigma[1], sigma[1]**2]
])

# 优化目标收益 10% 的最小方差组合
target_return = 0.10
constraints_with_return = (
    {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
    {'type': 'eq', 'fun': lambda w: w @ mu - target_return}
)
res_target = minimize(portfolio_variance, w0, constraints=constraints_with_return)
result['frontier_vol_at_target'] = np.sqrt(res_target.fun)

# 图形设置
plt.title('Efficient Frontier for Two Assets with Different Correlations')
plt.xlabel('Portfolio Volatility (Annualized)')
plt.ylabel('Portfolio Expected Return (Annualized)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = figure_path

# 输出结果（可选，便于调试）
print(result)
