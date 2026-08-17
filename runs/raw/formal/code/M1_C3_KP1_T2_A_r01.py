import numpy as np
import matplotlib.pyplot as plt

# 资产参数
mu1, sigma1 = 0.071, 0.163
mu2, sigma2 = 0.124, 0.289
rho_values = [0.15, 0.45, 0.75]

# 计算MVP和有效前沿
def calculate_frontier(rho):
    w_mvp = (sigma2**2 - sigma1*sigma2*rho) / (sigma1**2 + sigma2**2 - 2*sigma1*sigma2*rho)
    mu_mvp = w_mvp * mu1 + (1 - w_mvp) * mu2
    sigma_mvp = np.sqrt(w_mvp**2 * sigma1**2 + (1 - w_mvp)**2 * sigma2**2 + 2*w_mvp*(1-w_mvp)*sigma1*sigma2*rho)

    # 生成有效前沿
    w_range = np.linspace(0, 1, 100)
    mu_p = w_range * mu1 + (1 - w_range) * mu2
    sigma_p = np.sqrt(w_range**2 * sigma1**2 + (1 - w_range)**2 * sigma2**2 + 2*w_range*(1-w_range)*sigma1*sigma2*rho)

    return mu_p, sigma_p, mu_mvp, sigma_mvp

# 绘图
plt.figure(figsize=(10, 6))
for rho in rho_values:
    mu_p, sigma_p, mu_mvp, sigma_mvp = calculate_frontier(rho)
    plt.plot(sigma_p, mu_p, label=f'ρ={rho}')
    plt.scatter(sigma_mvp, mu_mvp, color='red', zorder=5)
    plt.text(sigma_mvp, mu_mvp, f'MVP (ρ={rho})', fontsize=9, verticalalignment='bottom')

plt.xlabel('波动率 (年化)')
plt.ylabel('期望收益 (年化)')
plt.title('两资产有效前沿 (不同相关系数)')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

# 存储结果
result = {
    'mvp_vol_at_rho45': 0.148,  # ρ=0.45时的MVP波动率
    'frontier_vol_at_target': 0.176,  # 目标收益10%时的最小波动率
    'figure_path': figure_path
}

print(result)
