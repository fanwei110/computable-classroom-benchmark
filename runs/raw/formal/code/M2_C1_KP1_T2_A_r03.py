import numpy as np
import matplotlib.pyplot as plt

# 资产参数
mu = np.array([0.071, 0.124])
sigma = np.array([0.163, 0.289])
rhos = [0.15, 0.45, 0.75]
target_return = 0.10

def min_var_weight(rho):
    """返回资产1在最小方差组合中的权重"""
    cov = rho * sigma[0] * sigma[1]
    w1 = (sigma[1]**2 - cov) / (sigma[0]**2 + sigma[1]**2 - 2*cov)
    return w1

def port_stats(w, rho):
    """给定资产1权重和相关系数，返回组合期望收益和波动率"""
    w1 = w
    w2 = 1 - w
    mu_p = w1 * mu[0] + w2 * mu[1]
    var = w1**2 * sigma[0]**2 + w2**2 * sigma[1]**2 + 2*w1*w2*rho*sigma[0]*sigma[1]
    return mu_p, np.sqrt(var)

# 计算所需指标
# 1) ρ=0.45 时最小方差组合的波动率
w_mvp_045 = min_var_weight(0.45)
_, vol_mvp_045 = port_stats(w_mvp_045, 0.45)

# 2) 目标收益10%时 ρ=0.45 前沿上的最小波动率
w_target = (target_return - mu[1]) / (mu[0] - mu[1])
_, vol_target = port_stats(w_target, 0.45)

# 构建结果字典
result = {
    'mvp_vol_at_rho45': vol_mvp_045,
    'frontier_vol_at_target': vol_target,
    'figure_path': './efficient_frontier.png'
}

# 绘制图像
fig, ax = plt.subplots(figsize=(8, 5))
ws = np.linspace(0, 1, 200)

for rho in rhos:
    mus, vols = port_stats(ws, rho)
    ax.plot(vols, mus, label=f'ρ = {rho}')
    # 标出最小方差组合
    w_mvp = min_var_weight(rho)
    mu_mvp, vol_mvp = port_stats(w_mvp, rho)
    ax.plot(vol_mvp, mu_mvp, 'o', markersize=8)

ax.set_xlabel('Volatility (Standard Deviation)')
ax.set_ylabel('Expected Return')
ax.set_title('Efficient Frontiers with Different Correlations')
ax.legend()
ax.grid(True)

plt.savefig(result['figure_path'])
plt.show()

print(result)
