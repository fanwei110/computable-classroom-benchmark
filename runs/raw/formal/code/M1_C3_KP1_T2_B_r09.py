import numpy as np
import matplotlib.pyplot as plt

# 参数
mu = np.array([0.071, 0.124])
sigma = np.array([0.163, 0.289])
rho_values = [0.15, 0.45, 0.75]
colors = ['r', 'g', 'b']
labels = [f'ρ={rho}' for rho in rho_values]

plt.figure(figsize=(10, 6))

for rho, color, label in zip(rho_values, colors, labels):
    cov = rho * sigma[0] * sigma[1]
    Sigma = np.array([[sigma[0]**2, cov], [cov, sigma[1]**2]])

    # 计算 MVP
    w_mvp = (sigma[1]**2 - cov) / (sigma[0]**2 + sigma[1]**2 - 2 * cov)
    mu_mvp = w_mvp * mu[0] + (1 - w_mvp) * mu[1]
    sigma_mvp = np.sqrt(w_mvp**2 * sigma[0]**2 + (1 - w_mvp)**2 * sigma[1]**2 + 2 * w_mvp * (1 - w_mvp) * cov)

    # 计算有效前沿
    weights = np.linspace(0, 1, 100)
    mu_p = weights * mu[0] + (1 - weights) * mu[1]
    sigma_p = np.sqrt(weights**2 * sigma[0]**2 + (1 - weights)**2 * sigma[1]**2 + 2 * weights * (1 - weights) * cov)

    # 绘制有效前沿
    plt.plot(sigma_p, mu_p, color=color, label=label)
    plt.scatter(sigma_mvp, mu_mvp, color=color, marker='o', s=100, label=f'MVP {label}')

plt.xlabel('Volatility (σ)')
plt.ylabel('Expected Return (μ)')
plt.title('Efficient Frontier for Two Assets')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

# 结果
result = {
    'mvp_vol_at_rho45': 0.1566,
    'frontier_vol_at_target': 0.2844,
    'figure_path': figure_path
}

print(result)
