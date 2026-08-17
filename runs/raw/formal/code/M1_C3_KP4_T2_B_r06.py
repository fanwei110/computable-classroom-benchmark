import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    """
    计算Black-Scholes期权Delta
    S: 标的价格
    K: 行权价
    T: 年化到期时间
    r: 无风险利率（连续复利）
    sigma: 波动率
    option_type: 'call'或'put'
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
T = 0.58  # 年化到期时间
vols = [0.15, 0.276, 0.40]  # 波动率列表
S_range = np.linspace(70, 140, 100)  # 标的价格范围

# 计算Delta曲线
plt.figure(figsize=(10, 6))
for vol in vols:
    deltas = [black_scholes_delta(S, K, T, r, vol) for S in S_range]
    plt.plot(S_range, deltas, label=f'Vol = {vol*100:.1f}%')

# 计算特定点的Delta
S_110 = 110
vol_276 = 0.276
delta_at_110 = black_scholes_delta(S_110, K, T, r, vol_276)

# 图形设置
plt.axvline(x=K, color='gray', linestyle='--', alpha=0.5)
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.title('Delta Curve for Different Volatilities')
plt.xlabel('Underlying Price')
plt.ylabel('Delta')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path)
plt.close()

# 存储结果
result = {
    'delta_at_s110': delta_at_110,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
