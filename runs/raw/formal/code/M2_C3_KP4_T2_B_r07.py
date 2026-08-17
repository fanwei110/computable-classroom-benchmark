import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# 参数设置（全部采用小数）
K = 97.5              # 行权价
r = 0.043             # 无风险利率（连续复利）
T = 0.58              # 到期时间（年）
sigmas = [0.15, 0.276, 0.40]  # 波动率
S_range = np.linspace(70, 140, 200)

# 计算看涨期权 Delta 的函数
def delta_call(S, sigma, K, r, T):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 绘图
plt.figure(figsize=(10, 6))
for sig in sigmas:
    delta_vals = delta_call(S_range, sig, K, r, T)
    plt.plot(S_range, delta_vals, label=f'vol = {sig*100:.1f}%')

plt.xlabel('Underlying Price (S)')
plt.ylabel('Delta')
plt.title('Call Option Delta Curves')
plt.legend()
plt.grid(True)
plt.tight_layout()

# 保存图片
fig_path = 'delta_curve.png'
plt.savefig(fig_path)
plt.close()

# 计算指定点的 Delta：S=110, vol=27.6%
delta_110 = delta_call(110, 0.276, K, r, T)

# 输出契约
result = {
    'delta_at_s110': round(delta_110, 4),
    'figure_path': fig_path
}

print(result)
