import numpy as np
import matplotlib.pyplot as plt
import os

# 资产参数
mu = np.array([0.071, 0.124])  # 期望收益
sigma = np.array([0.163, 0.289])  # 波动率

# 相关系数
rhos = [0.15, 0.45, 0.75]

# 计算协方差矩阵
def get_cov_matrix(rho):
    cov = np.array([
        [sigma[0]**2, sigma[0]*sigma[1]*rho],
        [sigma[0]*sigma[1]*rho, sigma[1]**2]
    ])
    return cov

# 计算最小方差组合
def calculate_mvp(cov):
    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)
    w = np.dot(cov_inv, ones) / np.dot(ones, np.dot(cov_inv, ones))
    mvp_vol = np.sqrt(np.dot(w, np.dot(cov, w)))
    mvp_ret = np.dot(w, mu)
    return w, mvp_ret, mvp_vol

# 计算有效前沿
def calculate_frontier(cov, target_returns=None, n_points=100):
    if target_returns is None:
        min_ret = min(mu)
        max_ret = max(mu)
        target_returns = np.linspace(min_ret, max_ret, n_points)

    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)

    # 计算有效前沿
    A = np.dot(ones, np.dot(cov_inv, ones))
    B = np.dot(ones, np.dot(cov_inv, mu))
    C = np.dot(mu, np.dot(cov_inv, mu))
    D = A * C - B**2

    weights = []
    vols = []
    rets = []

    for ret in target_returns:
        w = (C - B * ret) / D * np.dot(cov_inv, ones) + (A * ret - B) / D * np.dot(cov_inv, mu)
        vol = np.sqrt(np.dot(w, np.dot(cov, w)))
        weights.append(w)
        vols.append(vol)
        rets.append(ret)

    return np.array(rets), np.array(vols), np.array(weights)

# 绘制图形
plt.figure(figsize=(10, 6))

for rho in rhos:
    cov = get_cov_matrix(rho)
    rets, vols, weights = calculate_frontier(cov)

    # 绘制有效前沿
    plt.plot(vols, rets, label=f'ρ={rho}')

    # 计算并标记最小方差组合
    w_mvp, ret_mvp, vol_mvp = calculate_mvp(cov)
    plt.scatter(vol_mvp, ret_mvp, color='red')
    plt.text(vol_mvp, ret_mvp, f'MVP (ρ={rho})', fontsize=9, verticalalignment='bottom')

# 计算ρ=0.45时的特定结果
rho_45 = 0.45
cov_45 = get_cov_matrix(rho_45)
w_mvp_45, ret_mvp_45, vol_mvp_45 = calculate_mvp(cov_45)

# 计算目标收益10%时的最小波动率
target_ret = 0.10
rets_45, vols_45, weights_45 = calculate_frontier(cov_45, target_returns=[target_ret])
vol_at_target = vols_45[0]

# 保存图形
figure_path = 'efficient_frontier.png'
plt.title('Efficient Frontier with Different Correlations')
plt.xlabel('Volatility (Standard Deviation)')
plt.ylabel('Expected Return')
plt.legend()
plt.grid(True)
plt.savefig(figure_path)
plt.close()

# 准备结果
result = {
    'mvp_vol_at_rho45': vol_mvp_45,
    'frontier_vol_at_target': vol_at_target,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
