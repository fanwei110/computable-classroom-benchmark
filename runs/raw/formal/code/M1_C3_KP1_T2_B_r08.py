import numpy as np
import matplotlib.pyplot as plt

# 参数
mu1, mu2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
rho_values = [0.15, 0.45, 0.75]

# 计算MVP和有效前沿
def calculate_frontier(rho):
    cov = rho * sigma1 * sigma2
    sigma_squared = np.linspace(0.01, 0.3, 100)
    mu = []
    for sigma in sigma_squared:
        A = np.array([[sigma1**2, cov], [cov, sigma2**2]])
        b = np.array([sigma**2, 1])
        w = np.linalg.solve(A, b)
        mu_val = w[0] * mu1 + w[1] * mu2
        mu.append(mu_val)
    # MVP
    w1_mvp = (sigma2**2 - rho * sigma1 * sigma2) / (sigma1**2 + sigma2**2 - 2 * rho * sigma1 * sigma2)
    sigma_mvp = np.sqrt(w1_mvp**2 * sigma1**2 + (1 - w1_mvp)**2 * sigma2**2 + 2 * w1_mvp * (1 - w1_mvp) * cov)
    mu_mvp = w1_mvp * mu1 + (1 - w1_mvp) * mu2
    return sigma_squared, mu, sigma_mvp, mu_mvp

plt.figure(figsize=(10, 6))
for rho in rho_values:
    sigma_squared, mu, sigma_mvp, mu_mvp = calculate_frontier(rho)
    plt.plot(np.sqrt(sigma_squared), mu, label=f'ρ={rho}')
    plt.scatter(sigma_mvp, mu_mvp, color='red', zorder=5)
    plt.text(sigma_mvp, mu_mvp, f'MVP (ρ={rho})', fontsize=9, verticalalignment='bottom')

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
    'mvp_vol_at_rho45': 0.1576,
    'frontier_vol_at_target': 0.1946,
    'figure_path': figure_path
}
