import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    return delta

# 参数设置
K = 97.5
r = 0.043
T = 0.58
vols = [0.15, 0.276, 0.40]
S_range = np.linspace(70, 140, 100)

# 计算delta曲线
deltas = {}
for vol in vols:
    deltas[vol] = [black_scholes_delta(S, K, T, r, vol) for S in S_range]

# 绘制图形
plt.figure(figsize=(10, 6))
for vol in vols:
    plt.plot(S_range, deltas[vol], label=f'Vol = {vol*100:.1f}%')

plt.axvline(x=K, color='gray', linestyle='--', alpha=0.5)
plt.title('Delta Curve for Call Option')
plt.xlabel('Underlying Price')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path)
plt.close()

# 计算S=110, vol=27.6%的delta
delta_at_s110 = black_scholes_delta(110, K, T, r, 0.276)

# 输出结果
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
