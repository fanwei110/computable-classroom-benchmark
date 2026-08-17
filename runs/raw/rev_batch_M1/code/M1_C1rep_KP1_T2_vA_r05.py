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
    ones = np.ones(2)
    sigma_inv = np.linalg.inv(sigma)
    w_mvp = ones @ sigma_inv / (ones @ sigma_inv @ ones)
    vol_mvp = np.sqrt(w_mvp @ sigma @ w_mvp)
    mu_mvp = w_mvp @ np.array([mu1, mu2])
    return w_mvp, mu_mvp, vol_mvp

# 计算有效前沿
def calculate_frontier(rho, target_mu=None):
    cov = rho * vol1 * vol2
    sigma = np.array([[vol1**2, cov], [cov, vol2**2]])
    ones = np.ones(2)
    mu = np.array([mu1, mu2])

    # 最小方差组合
    sigma_inv = np.linalg.inv(sigma)
    w_mvp = ones @ sigma_inv / (ones @ sigma_inv @ ones)
    mu_mvp = w_mvp @ mu
    vol_mvp = np.sqrt(w_mvp @ sigma @ w_mvp)

    # 有效前沿参数
    A = ones @ sigma_inv @ ones
    B = ones @ sigma_inv @ mu
    C = mu @ sigma_inv @ mu
    D = A * C - B**2

    if target_mu is None:
        # 生成一系列目标收益
        mus = np.linspace(mu_mvp, mu2, 50)
    else:
        mus = [target_mu]

    vols = []
    for mu_target in mus:
        vol = np.sqrt((A * mu_target**2 - 2 * B * mu_target + C) / D)
        vols.append(vol)

    return mus, vols, (mu_mvp, vol_mvp)

# 绘制图形
plt.figure(figsize=(10, 6))

for rho in rhos:
    mus, vols, (mu_mvp, vol_mvp) = calculate_frontier(rho)
    plt.plot(vols, mus, label=f'ρ={rho}')
    plt.scatter(vol_mvp, mu_mvp, color='red', zorder=5)
    plt.text(vol_mvp, mu_mvp, f'MVP (ρ={rho})', ha='right', va='bottom')

# 计算特定条件下的值
_, _, (_, mvp_vol_at_rho45) = calculate_mvp(0.45)
_, frontier_vols, _ = calculate_frontier(0.45, target_mu=0.10)
frontier_vol_at_target = frontier_vols[0]

# 图形设置
plt.title('Efficient Frontier with Different Correlations')
plt.xlabel('Portfolio Volatility (Annualized)')
plt.ylabel('Portfolio Expected Return (Annualized)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

# 准备结果
result = {
    'mvp_vol_at_rho45': mvp_vol_at_rho45,
    'frontier_vol_at_target': frontier_vol_at_target,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
