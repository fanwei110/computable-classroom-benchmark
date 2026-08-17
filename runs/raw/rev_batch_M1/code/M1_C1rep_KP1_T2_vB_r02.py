import numpy as np
import matplotlib.pyplot as plt
import os

# 资产参数
mu = np.array([7.1, 12.4])  # 收益率
vol = np.array([16.3, 28.9])  # 波动率
corr_list = [0.15, 0.45, 0.75]  # 相关系数列表

# 计算协方差矩阵
def get_cov_matrix(vol1, vol2, corr):
    cov = corr * vol1 * vol2
    return np.array([[vol1**2, cov], [cov, vol2**2]])

# 计算最小方差组合
def calculate_mvp(mu, cov):
    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)
    w = np.dot(cov_inv, ones) / np.dot(ones, np.dot(cov_inv, ones))
    mvp_vol = np.sqrt(np.dot(w, np.dot(cov, w)))
    mvp_ret = np.dot(w, mu)
    return w, mvp_ret, mvp_vol

# 计算有效前沿
def calculate_frontier(mu, cov, n_points=50):
    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)
    A = np.dot(ones, np.dot(cov_inv, ones))
    B = np.dot(ones, np.dot(cov_inv, mu))
    C = np.dot(mu, np.dot(cov_inv, mu))
    D = A * C - B**2

    ret_range = np.linspace(min(mu), max(mu), n_points)
    vol_range = []
    for r in ret_range:
        vol = np.sqrt((A * r**2 - 2 * B * r + C) / D)
        vol_range.append(vol)

    return ret_range, vol_range

# 计算目标收益下的最小波动率
def calculate_min_vol_for_target(mu, cov, target_ret):
    ones = np.ones(2)
    cov_inv = np.linalg.inv(cov)
    A = np.dot(ones, np.dot(cov_inv, ones))
    B = np.dot(ones, np.dot(cov_inv, mu))
    C = np.dot(mu, np.dot(cov_inv, mu))
    D = A * C - B**2

    min_vol = np.sqrt((A * target_ret**2 - 2 * B * target_ret + C) / D)
    return min_vol

# 主计算
result = {}
plt.figure(figsize=(10, 6))

for corr in corr_list:
    cov = get_cov_matrix(vol[0], vol[1], corr)
    ret_range, vol_range = calculate_frontier(mu, cov)
    w_mvp, mvp_ret, mvp_vol = calculate_mvp(mu, cov)

    # 绘制有效前沿
    plt.plot(vol_range, ret_range, label=f'ρ={corr}')

    # 标记最小方差点
    plt.scatter(mvp_vol, mvp_ret, color='red')
    plt.text(mvp_vol, mvp_ret, f'MVP (ρ={corr})', fontsize=9, verticalalignment='bottom')

    # 保存ρ=0.45时的MVP波动率
    if corr == 0.45:
        result['mvp_vol_at_rho45'] = float(mvp_vol)

# 计算目标收益10%时的最小波动率
cov_45 = get_cov_matrix(vol[0], vol[1], 0.45)
result['frontier_vol_at_target'] = float(calculate_min_vol_for_target(mu, cov_45, 10))

# 图形设置
plt.title('Efficient Frontier with Two Assets')
plt.xlabel('Portfolio Volatility (%)')
plt.ylabel('Portfolio Return (%)')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'efficient_frontier.png'
plt.savefig(figure_path)
result['figure_path'] = os.path.abspath(figure_path)

plt.close()
