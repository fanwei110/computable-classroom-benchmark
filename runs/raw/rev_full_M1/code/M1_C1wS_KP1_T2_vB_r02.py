import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# 设定参数
returns = np.array([0.071, 0.124])
vols = np.array([0.163, 0.289])
correlations = [0.15, 0.45, 0.75]
target_return = 0.10

# 结果字典
result = {}

# 1. 构造协方差矩阵并绘制有效前沿
plt.figure(figsize=(10, 6))

for rho in correlations:
    # 构造协方差矩阵
    cov_matrix = np.array([
        [vols[0]**2, vols[0] * vols[1] * rho],
        [vols[0] * vols[1] * rho, vols[1]**2]
    ])

    # 生成权重向量 (w1从0到1，w2=1-w1)
    weights = np.linspace(0, 1, 100)
    portfolio_returns = weights * returns[0] + (1 - weights) * returns[1]
    portfolio_vols = np.sqrt(
        weights**2 * cov_matrix[0, 0] +
        (1 - weights)**2 * cov_matrix[1, 1] +
        2 * weights * (1 - weights) * cov_matrix[0, 1]
    )

    # 绘制有效前沿
    plt.plot(portfolio_vols, portfolio_returns, label=f'ρ={rho}')

    # 2. 找到最小方差组合
    def portfolio_variance(w, cov_matrix):
        return w @ cov_matrix @ w

    # 约束：权重之和为1
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
    bounds = ((0, 1), (0, 1))

    # 初始猜测
    w0 = np.array([0.5, 0.5])

    # 优化
    res = minimize(portfolio_variance, w0, args=(cov_matrix,),
                   constraints=constraints, bounds=bounds)
    mvp_weights = res.x
    mvp_return = mvp_weights @ returns
    mvp_vol = np.sqrt(portfolio_variance(mvp_weights, cov_matrix))

    # 标记最小方差点
    plt.scatter(mvp_vol, mvp_return, color='red', zorder=5)
    plt.text(mvp_vol, mvp_return, f'MVP (ρ={rho})',
             fontsize=9, verticalalignment='bottom')

    # 3. 对于ρ=0.45，计算所需的两个波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = mvp_vol

        # 计算目标收益10%时的最小波动率
        def objective(w, cov_matrix):
            return w @ cov_matrix @ w

        constraints = (
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w: w @ returns - target_return}
        )
        res = minimize(objective, w0, args=(cov_matrix,),
                       constraints=constraints, bounds=bounds)
        optimal_weights = res.x
        result['frontier_vol_at_target'] = np.sqrt(objective(optimal_weights, cov_matrix))

# 图形设置
plt.title('Efficient Frontier for Two-Asset Portfolio')
plt.xlabel('Portfolio Volatility')
plt.ylabel('Portfolio Return')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = figure_path

# 显示结果（可选，因为题目要求保存到result）
print(result)
