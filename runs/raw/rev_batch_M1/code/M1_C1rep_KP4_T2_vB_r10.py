import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    """
    计算Black-Scholes期权的Delta
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

# 计算delta曲线
plt.figure(figsize=(10, 6))
for vol in vols:
    deltas = [black_scholes_delta(S, K, T, r, vol) for S in S_range]
    plt.plot(S_range, deltas, label=f'Vol = {vol*100:.1f}%')

# 标记S=110, vol=27.6%的delta值
vol_276 = 0.276
delta_at_110 = black_scholes_delta(110, K, T, r, vol_276)
plt.scatter(110, delta_at_110, color='red', zorder=5)
plt.text(110, delta_at_110 + 0.02, f'Δ={delta_at_110:.4f}',
         ha='center', va='bottom', color='red')

# 图形设置
plt.title('Delta Curve for Different Volatilities')
plt.xlabel('Underlying Price')
plt.ylabel('Delta')
plt.axvline(x=K, color='gray', linestyle='--', alpha=0.5)
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path)
plt.close()

# 创建结果字典
result = {
    'delta_at_s110': delta_at_110,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
