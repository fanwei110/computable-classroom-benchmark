import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ---------- 参数 ----------
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余期限（年）
q = 0.0           # 标的无分红

# 可调参数：波动率列表
sigmas = [0.15, 0.276, 0.40]

# 标的价格网格
S = np.linspace(70, 140, 500)

# ---------- 函数 ----------
def delta_call(S, K, T, r, q, sigma):
    """欧式看涨期权 delta (Black-Scholes)"""
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)          # 无分红时 delta = N(d1)

# ---------- 画图 ----------
plt.figure(figsize=(10, 6))
for sigma in sigmas:
    delta = delta_call(S, K, T, r, q, sigma)
    plt.plot(S, delta, label=f'$\sigma$ = {sigma*100:.1f}%')

plt.xlabel('Underlying Price S')
plt.ylabel('Delta')
plt.title('Black-Scholes Call Delta')
plt.legend()
plt.grid(True)

# 保存图形
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# ---------- 报告指定点的 delta ----------
S_target = 110.0
sigma_target = 0.276
delta_target = delta_call(S_target, K, T, r, q, sigma_target)

# ---------- 输出字典 ----------
result = {
    'delta_at_s110': delta_target,
    'figure_path': figure_path
}

print(result)
