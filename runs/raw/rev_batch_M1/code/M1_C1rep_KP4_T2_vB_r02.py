import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    """
    计算Black-Scholes模型下的期权Delta
    :param S: 标的价格
    :param K: 行权价
    :param T: 到期时间（年）
    :param r: 无风险利率
    :param sigma: 波动率
    :param option_type: 期权类型（'call'或'put'）
    :return: Delta值
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    return delta

# 参数设置
K = 97.5  # 行权价
r = 0.043  # 无风险利率
T = 0.58  # 到期时间（年）
vols = [0.15, 0.276, 0.40]  # 波动率列表
S_range = np.linspace(70, 140, 100)  # 标的价格范围

# 绘制Delta曲线
plt.figure(figsize=(10, 6))
for vol in vols:
    delta_values = [black_scholes_delta(S, K, T, r, vol) for S in S_range]
    plt.plot(S_range, delta_values, label=f'Vol = {vol*100:.1f}%')

# 标记S=110, vol=27.6%的Delta值
vol_276 = 0.276
delta_at_110 = black_scholes_delta(110, K, T, r, vol_276)
plt.scatter(110, delta_at_110, color='red', zorder=5)
plt.text(110, delta_at_110 + 0.02, f'Δ={delta_at_110:.4f}', ha='center', color='red')

# 图例和标签
plt.title('Delta Curve for Different Volatilities')
plt.xlabel('Underlying Price')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'delta_curve.png'
plt.savefig(figure_path)
plt.close()

# 输出结果
result = {
    'delta_at_s110': delta_at_110,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
