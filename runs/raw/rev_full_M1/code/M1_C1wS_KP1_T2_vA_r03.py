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

    # 生成组合权重（满仓约束 w1 + w2 = 1）
    n_points = 100
    w1 = np.linspace(-0.5, 1.5, n_points)  # 允许杠杆和空头
    w = np.column_stack([w1, 1 - w1])

    # 计算组合收益和波动率
    port_returns = w @ mu
    port_vols = np.sqrt(np.diag(w @ Sigma @ w.T))

    # 绘制有效前沿（上半部分）
    plt.plot(port_vols, port_returns, label=f'ρ={rho}')

    # 2. 找到最小方差组合（满仓约束）
    def portfolio_variance(w, Sigma):
        return w.T @ Sigma @ w

    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = ((-1, 2), (-1, 2))  # 允许杠杆和空头
    initial_guess = [0.5, 0.5]

    res = minimize(portfolio_variance, initial_guess, args=(Sigma,),
                   bounds=bounds, constraints=constraints)
    w_mvp = res.x
    mvp_vol = np.sqrt(portfolio_variance(w_mvp, Sigma))
    mvp_return = w_mvp @ mu

    # 标记最小方差组合
    plt.scatter(mvp_vol, mvp_return, color='red', zorder=5)
    plt.text(mvp_vol, mvp_return, 'MVP', fontsize=9,
             verticalalignment='bottom', horizontalalignment='right')

# 图形设置
plt.title('Efficient Frontier for Two Assets with Different Correlations')
plt.xlabel('Portfolio Volatility (Annualized)')
plt.ylabel('Portfolio Expected Return (Annualized)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

result['figure_path'] = figure_path

# 3. 计算 ρ=0.45 时的两个波动率
rho_45 = 0.45
Sigma_45 = np.array([
    [sigma[0]**2, rho_45 * sigma[0] * sigma[1]],
    [rho_45 * sigma[0] * sigma[1], sigma[1]**2]
])

# 最小方差组合
res_45 = minimize(portfolio_variance, initial_guess, args=(Sigma_45,),
                  bounds=bounds, constraints=constraints)
w_mvp_45 = res_45.x
mvp_vol_45 = np.sqrt(portfolio_variance(w_mvp_45, Sigma_45))
result['mvp_vol_at_rho45'] = float(mvp_vol_45)

# 目标收益 10% 时的最小波动率
target_return = 0.10

def portfolio_variance_with_target(w, Sigma, mu, target_return):
    port_return = w @ mu
    return w.T @ Sigma @ w + 1e6 * (port_return - target_return)**2  # 惩罚项

res_target = minimize(portfolio_variance_with_target, initial_guess,
                      args=(Sigma_45, mu, target_return),
                      bounds=bounds, constraints=constraints)
w_target = res_target.x
target_vol = np.sqrt(portfolio_variance(w_target, Sigma_45))
result['frontier_vol_at_target'] = float(target_vol)

# 输出结果
print(result)
