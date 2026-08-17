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

def calculate_and_plot_delta(K, T, r, sigma_values, S_range, s_target, sigma_target):
    """
    计算并绘制 Delta 曲线
    :param K: 行权价
    :param T: 剩余期限（年）
    :param r: 无风险利率
    :param sigma_values: 波动率列表
    :param S_range: 标的价格范围
    :param s_target: 目标标的价格
    :param sigma_target: 目标波动率
    :return: 包含结果的字典
    """
    # 创建结果字典
    result = {}

    # 计算目标点的 Delta
    delta_at_s110 = black_scholes_delta(s_target, K, T, r, sigma_target)
    result['delta_at_s110'] = float(delta_at_s110)

    # 准备绘图
    plt.figure(figsize=(10, 6))

    # 计算并绘制每条波动率曲线
    for sigma in sigma_values:
        deltas = [black_scholes_delta(S, K, T, r, sigma) for S in S_range]
        plt.plot(S_range, deltas, label=f'σ = {sigma*100:.1f}%')

    # 设置图形属性
    plt.title('European Call Option Delta vs Underlying Price')
    plt.xlabel('Underlying Price')
    plt.ylabel('Delta')
    plt.legend()
    plt.grid(True)

    # 保存图形
    figure_path = 'delta_curve.png'
    plt.savefig(figure_path)
    plt.close()

    result['figure_path'] = os.path.abspath(figure_path)

    return result

# 参数设置
K = 97.5  # 行权价
T = 0.58  # 剩余期限（年）
r = 0.043  # 无风险利率
sigma_values = [0.15, 0.276, 0.40]  # 波动率列表
S_range = np.linspace(70, 140, 100)  # 标的价格范围
s_target = 110  # 目标标的价格
sigma_target = 0.276  # 目标波动率

# 计算并绘图
result = calculate_and_plot_delta(K, T, r, sigma_values, S_range, s_target, sigma_target)

# 输出结果（实际使用时可以直接使用 result 字典）
print(result)
