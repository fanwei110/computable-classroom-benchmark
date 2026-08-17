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

def plot_delta_curves(K, T, r, sigmas, S_range=(70, 140), n_points=100):
    """
    绘制不同波动率下的 Delta 曲线
    :param K: 行权价
    :param T: 剩余期限（年）
    :param r: 无风险利率
    :param sigmas: 波动率列表
    :param S_range: 标的价格范围
    :param n_points: 价格点数
    :return: 保存的图片路径
    """
    S_values = np.linspace(S_range[0], S_range[1], n_points)
    plt.figure(figsize=(10, 6))

    for sigma in sigmas:
        deltas = [black_scholes_delta(S, K, T, r, sigma) for S in S_values]
        plt.plot(S_values, deltas, label=f'σ = {sigma*100:.1f}%')

    plt.title('European Call Option Delta vs Underlying Price')
    plt.xlabel('Underlying Price')
    plt.ylabel('Delta')
    plt.axvline(x=K, color='gray', linestyle='--', label='Strike Price')
    plt.legend()
    plt.grid(True)

    # 保存图片
    figure_path = 'delta_curves.png'
    plt.savefig(figure_path)
    plt.close()

    return figure_path

# 参数设置
strike_price = 97.5
time_to_maturity = 0.58
risk_free_rate = 0.043
volatilities = [0.15, 0.276, 0.40]
target_price = 110
target_volatility = 0.276

# 计算特定点的 Delta
delta_at_s110 = black_scholes_delta(
    S=target_price,
    K=strike_price,
    T=time_to_maturity,
    r=risk_free_rate,
    sigma=target_volatility
)

# 绘制 Delta 曲线
figure_path = plot_delta_curves(
    K=strike_price,
    T=time_to_maturity,
    r=risk_free_rate,
    sigmas=volatilities
)

# 准备结果
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果（供验证）
print(result)
