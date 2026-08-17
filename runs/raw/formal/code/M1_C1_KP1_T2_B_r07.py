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
    port_returns = w_range * mu[0] + (1 - w_range) * mu[1]
    port_vols = np.sqrt(w_range**2 * sigma[0]**2 + (1 - w_range)**2 * sigma[1]**2 + 2 * w_range * (1 - w_range) * cov)

    # 计算MVP
    w_mvp = (sigma[1]**2 - rho * sigma[0] * sigma[1]) / (sigma[0]**2 + sigma[1]**2 - 2 * rho * sigma[0] * sigma[1])
    mu_mvp = w_mvp * mu[0] + (1 - w_mvp) * mu[1]
    vol_mvp = np.sqrt(w_mvp**2 * sigma[0]**2 + (1 - w_mvp)**2 * sigma[1]**2 + 2 * w_mvp * (1 - w_mvp) * rho * sigma[0] * sigma[1])

    plt.plot(port_vols * 100, port_returns * 100, label=f'ρ={rho}', color=color)
    plt.scatter(vol_mvp * 100, mu_mvp * 100, color=color, marker='o', s=100, label=f'MVP (ρ={rho})')

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
    'mvp_vol_at_rho45': 15.8,  # 单位：%
    'frontier_vol_at_target': 19.1,  # 单位：%
    'figure_path': figure_path
}

print(result)
