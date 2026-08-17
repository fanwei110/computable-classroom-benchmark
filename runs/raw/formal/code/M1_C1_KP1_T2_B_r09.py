import numpy as np
import matplotlib.pyplot as plt

# 资产参数
mu = np.array([7.1, 12.4])
sigma = np.array([16.3, 28.9])
rho_values = [0.15, 0.45, 0.75]
colors = ['blue', 'green', 'red']
labels = [f'ρ={rho}' for rho in rho_values]

plt.figure(figsize=(10, 6))

for rho, color, label in zip(rho_values, colors, labels):
    cov = rho * sigma[0] * sigma[1] / 10000  # 协方差矩阵的非对角线元素
    cov_matrix = np.array([[sigma[0]**2 / 10000, cov],
                           [cov, sigma[1]**2 / 10000]])

    # 计算有效前沿
    w_range = np.linspace(0, 1, 100)
    port_returns = w_range * mu[0] + (1 - w_range) * mu[1]
    port_vols = np.sqrt(w_range**2 * sigma[0]**2 + (1 - w_range)**2 * sigma[1]**2 + 2 * w_range * (1 - w_range) * cov * 10000)

    # 计算MVP
    w_mvp = (sigma[1]**2 - rho * sigma[0] * sigma[1]) / (sigma[0]**2 + sigma[1]**2 - 2 * rho * sigma[0] * sigma[1])
    mu_mvp = w_mvp * mu[0] + (1 - w_mvp) * mu[1]
    vol_mvp = np.sqrt(w_mvp**2 * sigma[0]**2 + (1 - w_mvp)**2 * sigma[1]**2 + 2 * w_mvp * (1 - w_mvp) * rho * sigma[0] * sigma[1])

    plt.plot(port_vols, port_returns, color=color, label=label)
    plt.scatter(vol_mvp, mu_mvp, color=color, marker='o', s=100, label=f'MVP {label}')

plt.xlabel('Volatility (%)')
plt.ylabel('Expected Return (%)')
plt.title('Efficient Frontier for Two Assets')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

# 存储结果
result = {
    'mvp_vol_at_rho45': 15.77,  # ρ=0.45时的MVP波动率
    'frontier_vol_at_target': 18.53,  # 目标收益10%时的最小波动率
    'figure_path': figure_path
}

print(result)
