import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import os

def black_scholes_delta(S, K, T, r, sigma):
    """
    计算欧式看涨期权的delta
    S: 标的资产价格
    K: 行权价
    T: 剩余期限（年）
    r: 无风险利率（连续复利）
    sigma: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# 参数设置
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余期限（年）
S_range = np.linspace(70, 140, 100)  # 标的价格范围

# 波动率参数
sigmas = [0.15, 0.276, 0.40]  # 15%, 27.6%, 40%

# 计算delta曲线
plt.figure(figsize=(10, 6))
for sigma in sigmas:
    deltas = black_scholes_delta(S_range, K, T, r, sigma)
    plt.plot(S_range, deltas, label=f'σ = {sigma:.1%}')

# 图形设置
plt.title('European Call Option Delta vs Underlying Price')
plt.xlabel('Underlying Price')
plt.ylabel('Delta')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'option_delta_plot.png'
plt.savefig(figure_path)
plt.close()

# 计算特定点的delta
S_target = 110
sigma_target = 0.276
delta_at_s110 = black_scholes_delta(S_target, K, T, r, sigma_target)

# 准备结果
result = {
    'delta_at_s110': float(delta_at_s110),
    'figure_path': os.path.abspath(figure_path)
}

# 输出结果（供课堂展示）
print(f"Delta at S=110, σ=27.6%: {delta_at_s110:.4f}")
print(f"Figure saved to: {result['figure_path']}")
