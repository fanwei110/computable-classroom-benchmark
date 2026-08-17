import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

def black_scholes_delta(S, K, T, r, sigma, option_type='call'):
    """
    计算Black-Scholes期权的Delta
    S: 标的价格
    K: 行权价
    T: 剩余期限（年）
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
r = 0.043  # 无风险利率4.3%
T = 0.58  # 剩余期限0.58年
vols = [0.15, 0.276, 0.40]  # 波动率15%, 27.6%, 40%
S_range = np.linspace(70, 140, 100)  # 标的价格范围70到140

# 计算delta曲线
plt.figure(figsize=(10, 6))
for vol in vols:
    deltas = [black_scholes_delta(S, K, T, r, vol) for S in S_range]
    plt.plot(S_range, deltas, label=f'Vol = {vol*100:.1f}%')

# 计算标的110时vol=27.6%的delta
delta_at_110 = black_scholes_delta(110, K, T, r, 0.276)

# 图形设置
plt.title('Delta Curve for Call Option')
plt.xlabel('Underlying Price')
plt.ylabel('Delta')
plt.axvline(x=K, color='gray', linestyle='--', label='Strike Price')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path)
plt.close()

# 准备结果
result = {
    'delta_at_s110': delta_at_110,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
