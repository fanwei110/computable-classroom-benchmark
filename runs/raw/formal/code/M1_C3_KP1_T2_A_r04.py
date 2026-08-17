import numpy as np
import matplotlib.pyplot as plt
import os

# 参数
E1, E2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
target_return = 0.10
rhos = [0.15, 0.45, 0.75]

# 计算最小方差组合 (MVP)
def calculate_mvp(sigma1, sigma2, rho):
    numerator = sigma2**2 - sigma1 * sigma2 * rho
    denominator = sigma1**2 + sigma2**2 - 2 * sigma1 * sigma2 * rho
    w1 = numerator / denominator
    w2 = 1 - w1
    sigma_p = np.sqrt(w1**2 * sigma1**2 + w2**2 * sigma2**2 + 2 * w1 * w2 * sigma1 * sigma2 * rho)
    return w1, w2, sigma_p

# 计算给定收益下的最小波动率
def calculate_min_vol_for_target(E1, E2, sigma1, sigma2, rho, target_return):
    # 解方程组：E_p = w1*E1 + w2*E2, w1 + w2 = 1
    # 使得 sigma_p 最小
    A = np.array([
        [sigma1**2, sigma1 * sigma2 * rho],
        [sigma1 * sigma2 * rho, sigma2**2]
    ])
    b = np.array([E1 - E2, target_return - E2])
    w = np.linalg.solve(A, b)
    w1 = w[0]
    w2 = 1 - w1
    sigma_p = np.sqrt(w1**2 * sigma1**2 + w2**2 * sigma2**2 + 2 * w1 * w2 * sigma1 * sigma2 * rho)
    return sigma_p

# 计算有效前沿
def calculate_frontier(E1, E2, sigma1, sigma2, rho):
    weights = np.linspace(0, 1, 100)
    returns = weights * E1 + (1 - weights) * E2
    vols = np.sqrt(weights**2 * sigma1**2 + (1 - weights)**2 * sigma2**2 + 2 * weights * (1 - weights) * sigma1 * sigma2 * rho)
    return returns, vols

# 计算结果
result = {}
rho_45 = 0.45
w1_mvp, w2_mvp, mvp_vol_at_rho45 = calculate_mvp(sigma1, sigma2, rho_45)
result['mvp_vol_at_rho45'] = mvp_vol_at_rho45

frontier_vol_at_target = calculate_min_vol_for_target(E1, E2, sigma1, sigma2, rho_45, target_return)
result['frontier_vol_at_target'] = frontier_vol_at_target

# 绘图
plt.figure(figsize=(10, 6))
for rho in rhos:
    returns, vols = calculate_frontier(E1, E2, sigma1, sigma2, rho)
    plt.plot(vols, returns, label=f'ρ={rho}')

    # 标记 MVP
    w1_mvp, w2_mvp, mvp_vol = calculate_mvp(sigma1, sigma2, rho)
    mvp_return = w1_mvp * E1 + w2_mvp * E2
    plt.scatter(mvp_vol, mvp_return, color='red', zorder=5)
    plt.text(mvp_vol, mvp_return, f'MVP (ρ={rho})', fontsize=9, verticalalignment='bottom')

plt.title('Efficient Frontier for Two Assets')
plt.xlabel('Volatility (σ)')
plt.ylabel('Expected Return (E)')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = os.path.abspath(figure_path)

plt.close()
print(result)
