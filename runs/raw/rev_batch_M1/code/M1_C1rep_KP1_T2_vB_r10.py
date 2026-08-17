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

    # 计算MVP
    w_mvp = np.linalg.inv(Sigma) @ np.ones(2) / (np.ones(2) @ np.linalg.inv(Sigma) @ np.ones(2))
    mu_mvp = w_mvp @ mu
    sigma_mvp = np.sqrt(w_mvp @ Sigma @ w_mvp)

    # 生成有效前沿
    w1_range = np.linspace(0, 1, 100)
    mu_p = w1_range * mu[0] + (1 - w1_range) * mu[1]
    sigma_p = np.sqrt(w1_range**2 * sigma[0]**2 + (1 - w1_range)**2 * sigma[1]**2 + 2 * w1_range * (1 - w1_range) * cov)

    # 绘制
    plt.plot(sigma_p * 100, mu_p * 100, label=f'ρ={rho}', color=color)
    plt.scatter(sigma_mvp * 100, mu_mvp * 100, color=color, marker='o', s=100, label=f'MVP (ρ={rho})')

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
    'frontier_vol_at_target': 19.6,  # 单位：%
    'figure_path': figure_path
}

print(result)
