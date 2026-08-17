import numpy as np
import matplotlib.pyplot as plt
import os

# 参数
E1, E2 = 0.071, 0.124
sigma1, sigma2 = 0.163, 0.289
target_return = 0.10

# 相关系数
rhos = [0.15, 0.45, 0.75]

# 计算最小方差组合 (MVP)
def calculate_mvp(sigma1, sigma2, rho):
    w1 = (sigma2**2 - sigma1 * sigma2 * rho) / (sigma1**2 + sigma2**2 - 2 * sigma1 * sigma2 * rho)
    w2 = 1 - w1
    sigma_p = np.sqrt(w1**2 * sigma1**2 + w2**2 * sigma2**2 + 2 * w1 * w2 * sigma1 * sigma2 * rho)
    return w1, w2, sigma_p

# 计算给定目标收益下的最小波动率
def calculate_min_vol_for_target(E1, E2, sigma1, sigma2, rho, target_return):
    # 解方程组：E(R_p) = w1*E1 + w2*E2 = target_return, w1 + w2 = 1
    # 最小化 sigma_p^2 = w1^2*sigma1^2 + w2^2*sigma2^2 + 2*w1*w2*sigma1*sigma2*rho
    # 使用拉格朗日乘数法
    A = np.array([
        [sigma1**2, sigma1*sigma2*rho],
        [sigma1*sigma2*rho, sigma2**2]
    ])
    B = np.array([E1, E2])
    C = np.array([1, 1])
    D = np.array([target_return, 1])

    # 解线性方程组
    inv_A = np.linalg.inv(A)
    lambda1 = (D[0] - B @ inv_A @ C) / (B @ inv_A @ B)
    lambda2 = (D[1] - C @ inv_A @ B) / (C @ inv_A @ C)
    w = inv_A @ (lambda1 * B + lambda2 * C)
    w1, w2 = w[0], w[1]
    sigma_p = np.sqrt(w1**2 * sigma1**2 + w2**2 * sigma2**2 + 2 * w1 * w2 * sigma1 * sigma2 * rho)
    return w1, w2, sigma_p

# 计算并绘制有效前沿
plt.figure(figsize=(10, 6))
result = {}

for rho in rhos:
    # 计算 MVP
    w1_mvp, w2_mvp, sigma_mvp = calculate_mvp(sigma1, sigma2, rho)
    E_mvp = w1_mvp * E1 + w2_mvp * E2

    # 计算有效前沿上的点
    weights = np.linspace(0, 1, 100)
    E_p = weights * E1 + (1 - weights) * E2
    sigma_p = np.sqrt(weights**2 * sigma1**2 + (1 - weights)**2 * sigma2**2 + 2 * weights * (1 - weights) * sigma1 * sigma2 * rho)

    # 绘制有效前沿
    plt.plot(sigma_p, E_p, label=f'ρ={rho}')
    plt.scatter(sigma_mvp, E_mvp, color='red', zorder=5)
    plt.text(sigma_mvp, E_mvp, f'MVP (ρ={rho})', fontsize=9, verticalalignment='bottom')

    # 存储 ρ=0.45 时的 MVP 波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = sigma_mvp

# 计算 ρ=0.45 时目标收益为10%的最小波动率
w1_target, w2_target, sigma_target = calculate_min_vol_for_target(E1, E2, sigma1, sigma2, 0.45, target_return)
result['frontier_vol_at_target'] = sigma_target

# 图形设置
plt.title('Efficient Frontier for Two Assets with Different Correlations')
plt.xlabel('Volatility (σ)')
plt.ylabel('Expected Return (E)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = os.path.abspath(figure_path)

plt.close()
print(result)
