import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

def black_scholes_call_delta(S, K, T, r, sigma):
    """
    计算欧式看涨期权的Delta
    S: 标的资产价格
    K: 行权价
    T: 剩余期限（年）
    r: 无风险利率
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

def plot_delta_curves(K, T, r, sigmas, S_range=(70, 140), S_points=100):
    """
    绘制不同波动率下的Delta曲线
    """
    S_values = np.linspace(S_range[0], S_range[1], S_points)
    plt.figure(figsize=(10, 6))

    for sigma in sigmas:
        deltas = [black_scholes_call_delta(S, K, T, r, sigma) for S in S_values]
        plt.plot(S_values, deltas, label=f'Volatility = {sigma*100:.1f}%')

    plt.title('European Call Option Delta vs Underlying Price')
    plt.xlabel('Underlying Price')
    plt.ylabel('Delta')
    plt.legend()
    plt.grid(True)

    # 保存图形
    figure_path = 'delta_curves.png'
    plt.savefig(figure_path)
    plt.close()

    return figure_path

# 参数设置
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余期限（年）
sigmas = [0.15, 0.276, 0.40]  # 波动率列表
S_target = 110    # 目标标的价格
sigma_target = 0.276  # 目标波动率

# 计算目标点的Delta
delta_at_s110 = black_scholes_call_delta(S_target, K, T, r, sigma_target)

# 绘制Delta曲线
figure_path = plot_delta_curves(K, T, r, sigmas)

# 准备结果
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果（供检查）
print(result)
