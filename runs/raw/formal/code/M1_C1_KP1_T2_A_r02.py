import numpy as np
import matplotlib.pyplot as plt
import os

# 资产参数
mu1, mu2 = 0.071, 0.124
vol1, vol2 = 0.163, 0.289

# 相关系数
rhos = [0.15, 0.45, 0.75]

# 计算最小方差组合
def calculate_mvp(rho):
    cov = rho * vol1 * vol2
    sigma = np.array([[vol1**2, cov], [cov, vol2**2]])
    ones = np.array([1, 1])
    sigma_inv = np.linalg.inv(sigma)
    w_mvp = ones @ sigma_inv / (ones @ sigma_inv @ ones)
    vol_mvp = np.sqrt(w_mvp @ sigma @ w_mvp)
    mu_mvp = w_mvp @ np.array([mu1, mu2])
    return w_mvp, mu_mvp, vol_mvp

# 计算有效前沿
def calculate_frontier(rho, n_points=100):
    cov = rho * vol1 * vol2
    sigma = np.array([[vol1**2, cov], [cov, vol2**2]])
    ones = np.array([1, 1])
    sigma_inv = np.linalg.inv(sigma)

    # 最小方差组合
    w_mvp = ones @ sigma_inv / (ones @ sigma_inv @ ones)
    mu_mvp = w_mvp @ np.array([mu1, mu2])
    vol_mvp = np.sqrt(w_mvp @ sigma @ w_mvp)

    # 有效前沿点
    mus = np.linspace(mu_mvp, mu2, n_points)
    vols = []
    for mu in mus:
        A = ones @ sigma_inv @ ones
        B = ones @ sigma_inv @ np.array([mu1, mu2])
        C = np.array([mu1, mu2]) @ sigma_inv @ np.array([mu1, mu2])
        D = A * C - B**2
        lambda_ = (C - B * mu) / D
        gamma = (A * mu - B) / D
        w = lambda_ * (sigma_inv @ ones) + gamma * (sigma_inv @ np.array([mu1, mu2]))
        vol = np.sqrt(w @ sigma @ w)
        vols.append(vol)

    return mus, vols, (mu_mvp, vol_mvp)

# 计算目标收益10%时的最小波动率
def calculate_vol_at_target(rho, target_return=0.10):
    cov = rho * vol1 * vol2
    sigma = np.array([[vol1**2, cov], [cov, vol2**2]])
    ones = np.array([1, 1])
    sigma_inv = np.linalg.inv(sigma)

    A = ones @ sigma_inv @ ones
    B = ones @ sigma_inv @ np.array([mu1, mu2])
    C = np.array([mu1, mu2]) @ sigma_inv @ np.array([mu1, mu2])
    D = A * C - B**2

    lambda_ = (C - B * target_return) / D
    gamma = (A * target_return - B) / D
    w = lambda_ * (sigma_inv @ ones) + gamma * (sigma_inv @ np.array([mu1, mu2]))
    vol = np.sqrt(w @ sigma @ w)

    return vol

# 绘制图形
plt.figure(figsize=(10, 6))

for rho in rhos:
    mus, vols, mvp = calculate_frontier(rho)
    plt.plot(vols, mus, label=f'ρ={rho}')
    plt.scatter(mvp[1], mvp[0], color='red', zorder=5)
    plt.text(mvp[1], mvp[0], f'MVP (ρ={rho})', fontsize=9,
             verticalalignment='bottom', horizontalalignment='right')

plt.title('Efficient Frontier with Different Correlations')
plt.xlabel('Portfolio Volatility (Annualized)')
plt.ylabel('Portfolio Expected Return (Annualized)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

# 计算结果
mvp_vol_at_rho45 = calculate_mvp(0.45)[2]
frontier_vol_at_target = calculate_vol_at_target(0.45, 0.10)

# 创建结果字典
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
