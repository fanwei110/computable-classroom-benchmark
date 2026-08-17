import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# ---------- 参数 ----------
K = 97.5                # 行权价
r = 0.043               # 无风险利率
T = 0.58                # 到期时间（年）
vol_list = [0.15, 0.276, 0.40]   # 波动率列表
S_grid = np.linspace(70, 140, 500)  # 标的网格

# ---------- 计算 Delta（欧式看涨期权） ----------
def delta_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ---------- 绘图 ----------
plt.figure(figsize=(8, 5))
for sigma in vol_list:
    delta = delta_call(S_grid, K, T, r, sigma)
    plt.plot(S_grid, delta, label=f'vol={sigma*100:.1f}%')

plt.xlabel('Underlying Price S')
plt.ylabel('Delta')
plt.title('Black-Scholes Call Delta')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 保存图片
fig_path = 'delta_curves.png'
plt.savefig(fig_path)
plt.close()

# ---------- 特定点 Delta ----------
S_target = 110
sigma_target = 0.276
delta_target = delta_call(S_target, K, T, r, sigma_target)

# ---------- 输出结果 ----------
result = {
    'delta_at_s110': delta_target,
    'figure_path': fig_path
}

print(result)
