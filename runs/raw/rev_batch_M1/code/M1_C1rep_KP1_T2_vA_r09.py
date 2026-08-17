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
        [sigma[0]**2, rho * sigma[0] * sigma[1]],
        [rho * sigma[0] * sigma[1], sigma[1]**2]
    ])
    return cov

# 计算最小方差组合
def calculate_mvp(cov):
    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)
    w = cov_inv @ ones / (ones @ cov_inv @ ones)
    mvp_vol = np.sqrt(w @ cov @ w)
    mvp_ret = w @ mu
    return w, mvp_ret, mvp_vol

# 计算有效前沿
def calculate_frontier(cov, target_returns=None):
    if target_returns is None:
        target_returns = np.linspace(mu.min(), mu.max(), 100)

    cov_inv = np.linalg.inv(cov)
    ones = np.ones(2)

    A = ones @ cov_inv @ ones
    B = ones @ cov_inv @ mu
    C = mu @ cov_inv @ mu
    D = A * C - B**2

    weights = []
    vols = []
    rets = []

    for ret in target_returns:
        w = (C - B * ret) * cov_inv @ ones / D + (A * ret - B) * cov_inv @ mu / D
        vol = np.sqrt(w @ cov @ w)
        weights.append(w)
        vols.append(vol)
        rets.append(ret)

    return np.array(rets), np.array(vols), np.array(weights)

# 绘图
plt.figure(figsize=(10, 6))

result = {}

for rho in rhos:
    cov = get_cov_matrix(rho)
    rets, vols, weights = calculate_frontier(cov)

    # 计算MVP
    mvp_w, mvp_ret, mvp_vol = calculate_mvp(cov)

    # 保存rho=0.45时的MVP波动率
    if rho == 0.45:
        result['mvp_vol_at_rho45'] = float(mvp_vol)

    # 绘制前沿
    plt.plot(vols, rets, label=f'ρ={rho}')

    # 标记MVP
    plt.scatter(mvp_vol, mvp_ret, color='red', zorder=5)
    plt.text(mvp_vol, mvp_ret, f'MVP (ρ={rho})', fontsize=9,
             verticalalignment='bottom', horizontalalignment='right')

# 计算目标收益10%时的最小波动率
rho = 0.45
cov = get_cov_matrix(rho)
target_ret = 0.10
rets, vols, weights = calculate_frontier(cov, target_returns=np.array([target_ret]))
result['frontier_vol_at_target'] = float(vols[0])

# 图形设置
plt.title('Efficient Frontier with Different Correlations')
plt.xlabel('Volatility (Standard Deviation)')
plt.ylabel('Expected Return')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
plt.close()

result['figure_path'] = os.path.abspath(figure_path)

print(result)
