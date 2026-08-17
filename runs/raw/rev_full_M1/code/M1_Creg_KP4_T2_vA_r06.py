import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    """
    计算 Black-Scholes 模型下的期权 Delta
    :param S: 标的资产价格
    :param K: 行权价
    :param T: 剩余期限（年）
    :param r: 无风险利率
    :param sigma: 波动率
    :param option_type: 期权类型（'call' 或 'put'）
    :return: Delta 值
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    return delta

def generate_delta_curve():
    # 参数设置
    K = 97.5  # 行权价
    r = 0.043  # 无风险利率
    T = 0.58  # 剩余期限（年）
    S_range = np.linspace(70, 140, 100)  # 标的价格范围

    # 波动率设置
    sigma_values = [0.15, 0.276, 0.40]
    sigma_labels = ['15%', '27.6%', '40%']

    # 创建图形
    plt.figure(figsize=(10, 6))

    # 计算并绘制每条波动率对应的 delta 曲线
    for sigma, label in zip(sigma_values, sigma_labels):
        delta_values = [black_scholes_delta(S, K, T, r, sigma) for S in S_range]
        plt.plot(S_range, delta_values, label=f'Volatility = {label}')

    # 图形设置
    plt.title('Delta of European Call Option')
    plt.xlabel('Underlying Price')
    plt.ylabel('Delta')
    plt.legend()
    plt.grid(True)

    # 保存图形
    figure_path = 'delta_curve.png'
    plt.savefig(figure_path)
    plt.close()

    # 计算特定点的 delta
    S_target = 110
    sigma_target = 0.276
    delta_at_s110 = black_scholes_delta(S_target, K, T, r, sigma_target)

    # 返回结果
    result = {
        'delta_at_s110': delta_at_s110,
        'figure_path': os.path.abspath(figure_path)
    }

    return result

# 执行并输出结果
result = generate_delta_curve()
print(result)
