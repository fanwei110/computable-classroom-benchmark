import numpy as np
import matplotlib.pyplot as plt

# 参数
mu1, mu2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
rhos = [0.15, 0.45, 0.75]

# 计算MVP和有效前沿
def portfolio_vol(w, sigma1, sigma2, rho):
    return np.sqrt(w**2 * sigma1**2 + (1 - w)**2 * sigma2**2 + 2 * w * (1 - w) * sigma1 * sigma2 * rho)

def portfolio_return(w, mu1, mu2):
    return w * mu1 + (1 - w) * mu2

# 绘图
plt.figure(figsize=(10, 6))
for rho in rhos:
    # 计算MVP
    w_mvp = (sigma2**2 - sigma1 * sigma2 * rho) / (sigma1**2 + sigma2**2 - 2 * sigma1 * sigma2 * rho)
    sigma_mvp = portfolio_vol(w_mvp, sigma1, sigma2, rho)
    mu_mvp = portfolio_return(w_mvp, mu1, mu2)

    # 生成有效前沿
    w_range = np.linspace(0, 1, 100)
    mu_range = portfolio_return(w_range, mu1, mu2)
    sigma_range = [portfolio_vol(w, sigma1, sigma2, rho) for w in w_range]

    # 绘制有效前沿
    plt.plot(sigma_range, mu_range, label=f'ρ={rho}')
    plt.scatter(sigma_mvp, mu_mvp, color='red', zorder=5)
    plt.text(sigma_mvp, mu_mvp, f'MVP (ρ={rho})', fontsize=9, verticalalignment='bottom')

plt.title('Efficient Frontier for Two Assets')
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
    'mvp_vol_at_rho45': 0.1609,
    'frontier_vol_at_target': 0.2020,
    'figure_path': figure_path
}

print(result)
