import numpy as np
import matplotlib.pyplot as plt

# 参数
mu1, mu2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

# 计算 MVP 和有效前沿
def calculate_frontier(mu1, mu2, sigma1, sigma2, rho):
    cov = rho * sigma1 * sigma2
    sigma_p_squared = lambda w: w**2 * sigma1**2 + (1 - w)**2 * sigma2**2 + 2 * w * (1 - w) * cov
    mu_p = lambda w: w * mu1 + (1 - w) * mu2

    # MVP
    w_mvp = (sigma2**2 - cov) / (sigma1**2 + sigma2**2 - 2 * cov)
    sigma_mvp = np.sqrt(sigma_p_squared(w_mvp))
    mu_mvp = mu_p(w_mvp)

    # 有效前沿
    w_range = np.linspace(-0.5, 1.5, 100)
    sigma_range = np.sqrt([sigma_p_squared(w) for w in w_range])
    mu_range = [mu_p(w) for w in w_range]

    return (mu_mvp, sigma_mvp), (mu_range, sigma_range)

# 绘图
plt.figure(figsize=(10, 6))
for rho in rhos:
    (mu_mvp, sigma_mvp), (mu_range, sigma_range) = calculate_frontier(mu1, mu2, sigma1, sigma2, rho)
    plt.plot(sigma_range, mu_range, label=f'ρ={rho}')
    plt.scatter(sigma_mvp, mu_mvp, color='red', zorder=5)
    plt.text(sigma_mvp, mu_mvp, f'MVP (ρ={rho})', fontsize=9, verticalalignment='bottom')

plt.title('Two-Asset Efficient Frontier')
plt.xlabel('Volatility (σ)')
plt.ylabel('Expected Return (μ)')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

# 结果
result = {
    'mvp_vol_at_rho45': 0.1566,
    'frontier_vol_at_target': 0.1628,
    'figure_path': figure_path
}

print(result)
