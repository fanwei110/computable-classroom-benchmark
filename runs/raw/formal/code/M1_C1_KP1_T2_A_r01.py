import numpy as np
import matplotlib.pyplot as plt
import os

# 资产参数
mu = np.array([0.071, 0.124])  # 期望收益
sigma = np.array([0.163, 0.289])  # 波动率

# 相关系数
rhos = [0.15, 0.45, 0.75]

# 计算协方差矩阵
def get_cov_matrix(rho):
    cov = np.array([
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [rho * sigma[0] * sigma[1], sigma[1]**2]
    ])
    return cov

# 计算最小方差组合
def calculate_mvp(cov):
    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)
    w_mvp = ones @ cov_inv / (ones @ cov_inv @ ones)
    mu_mvp = w_mvp @ mu
    sigma_mvp = np.sqrt(w_mvp @ cov @ w_mvp)
    return w_mvp, mu_mvp, sigma_mvp

# 计算有效前沿
def calculate_frontier(cov, n_points=100):
    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)

    # 最小方差组合
    w_mvp = ones @ cov_inv / (ones @ cov_inv @ ones)
    mu_mvp = w_mvp @ mu
    sigma_mvp = np.sqrt(w_mvp @ cov @ w_mvp)

    # 有效前沿
    mu_range = np.linspace(mu_mvp, max(mu), n_points)
    sigma_frontier = []
    for target_mu in mu_range:
        A = ones @ cov_inv @ ones
        B = ones @ cov_inv @ mu
        C = mu @ cov_inv @ mu
        D = A * C - B**2
        lambda_ = (C - B * target_mu) / D
        gamma = (A * target_mu - B) / D
        w = lambda_ * (cov_inv @ ones) + gamma * (cov_inv @ mu)
        sigma_frontier.append(np.sqrt(w @ cov @ w))

    return mu_range, np.array(sigma_frontier), mu_mvp, sigma_mvp

# 绘制图形
plt.figure(figsize=(10, 6))

for rho in rhos:
    cov = get_cov_matrix(rho)
    mu_range, sigma_frontier, mu_mvp, sigma_mvp = calculate_frontier(cov)

    # 绘制有效前沿
    plt.plot(sigma_frontier, mu_range, label=f'ρ={rho}')

    # 标记最小方差组合
    plt.scatter(sigma_mvp, mu_mvp, color='red')
    plt.text(sigma_mvp, mu_mvp, f'MVP (ρ={rho})', fontsize=9, verticalalignment='bottom')

# 计算ρ=0.45时的特定结果
cov_45 = get_cov_matrix(0.45)
_, _, mu_mvp_45, sigma_mvp_45 = calculate_frontier(cov_45)
target_return = 0.10
mu_range_45, sigma_frontier_45, _, _ = calculate_frontier(cov_45)
idx = np.argmin(np.abs(mu_range_45 - target_return))
sigma_at_target = sigma_frontier_45[idx]

# 保存结果
result = {
    'mvp_vol_at_rho45': sigma_mvp_45,
    'frontier_vol_at_target': sigma_at_target,
    'figure_path': 'efficient_frontier.png'
}

# 完成图形
plt.title('Efficient Frontier with Different Correlations')
plt.xlabel('Portfolio Volatility (σ)')
plt.ylabel('Portfolio Expected Return (μ)')
plt.legend()
plt.grid(True)

# 保存图形
plt.savefig(result['figure_path'])
plt.close()

print(result)
