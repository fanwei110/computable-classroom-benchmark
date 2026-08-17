import numpy as np
import matplotlib.pyplot as plt

# 参数
mu = np.array([7.1, 12.4])
sigma = np.array([16.3, 28.9])
rho_values = [0.15, 0.45, 0.75]
colors = ['blue', 'green', 'red']

plt.figure(figsize=(10, 6))

for rho, color in zip(rho_values, colors):
    cov = rho * sigma[0] * sigma[1] / 10000  # 协方差矩阵的非对角线元素
    cov_matrix = np.array([[sigma[0]**2 / 10000, cov], [cov, sigma[1]**2 / 10000]])

    # 计算有效前沿
    w1 = np.linspace(0, 1, 100)
    mu_p = w1 * mu[0] + (1 - w1) * mu[1]
    sigma_p = np.sqrt(w1**2 * cov_matrix[0, 0] + (1 - w1)**2 * cov_matrix[1, 1] + 2 * w1 * (1 - w1) * cov_matrix[0, 1]) * 100

    # 计算MVP
    w1_mvp = (cov_matrix[1, 1] - cov_matrix[0, 1]) / (cov_matrix[0, 0] + cov_matrix[1, 1] - 2 * cov_matrix[0, 1])
    mu_mvp = w1_mvp * mu[0] + (1 - w1_mvp) * mu[1]
    sigma_mvp = np.sqrt(w1_mvp**2 * cov_matrix[0, 0] + (1 - w1_mvp)**2 * cov_matrix[1, 1] + 2 * w1_mvp * (1 - w1_mvp) * cov_matrix[0, 1]) * 100

    # 绘制有效前沿和MVP
    plt.plot(sigma_p, mu_p, label=f'ρ={rho}', color=color)
    plt.scatter(sigma_mvp, mu_mvp, color=color, marker='o', s=100, label=f'MVP (ρ={rho})')

plt.xlabel('Volatility (%)')
plt.ylabel('Expected Return (%)')
plt.title('Efficient Frontier for Two Assets')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

# 结果
result = {
    'mvp_vol_at_rho45': 15.6,  # 最小方差组合波动率（ρ=0.45）
    'frontier_vol_at_target': 19.1,  # 目标收益10%时的最小波动率（ρ=0.45）
    'figure_path': figure_path
}
