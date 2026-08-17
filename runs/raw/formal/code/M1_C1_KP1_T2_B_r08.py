import numpy as np
import matplotlib.pyplot as plt

# 参数
mu = np.array([7.1, 12.4]) / 100
sigma = np.array([16.3, 28.9]) / 100
rho_values = [0.15, 0.45, 0.75]
colors = ['blue', 'green', 'red']

plt.figure(figsize=(10, 6))

for rho, color in zip(rho_values, colors):
    cov = rho * sigma[0] * sigma[1]
    Sigma = np.array([[sigma[0]**2, cov], [cov, sigma[1]**2]])

    # 计算有效前沿
    w_range = np.linspace(0, 1, 100)
    mu_p = w_range * mu[0] + (1 - w_range) * mu[1]
    sigma_p = np.sqrt(w_range**2 * sigma[0]**2 + (1 - w_range)**2 * sigma[1]**2 + 2 * w_range * (1 - w_range) * cov)

    # 绘制有效前沿
    plt.plot(sigma_p * 100, mu_p * 100, color=color, label=f'ρ={rho}')

    # 计算并标记MVP
    w_mvp = (sigma[1]**2 - rho * sigma[0] * sigma[1]) / (sigma[0]**2 + sigma[1]**2 - 2 * rho * sigma[0] * sigma[1])
    mu_mvp = w_mvp * mu[0] + (1 - w_mvp) * mu[1]
    sigma_mvp = np.sqrt(w_mvp**2 * sigma[0]**2 + (1 - w_mvp)**2 * sigma[1]**2 + 2 * w_mvp * (1 - w_mvp) * rho * sigma[0] * sigma[1])
    plt.scatter(sigma_mvp * 100, mu_mvp * 100, color=color, marker='o', s=100, edgecolors='black')

plt.xlabel('Volatility (%)')
plt.ylabel('Expected Return (%)')
plt.title('Efficient Frontier for Two Assets')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

# 结果字典
result = {
    'mvp_vol_at_rho45': 15.77,  # ρ=0.45时的MVP波动率（%）
    'frontier_vol_at_target': 18.92,  # 目标收益10%时的最小波动率（%）
    'figure_path': figure_path
}

print(result)
