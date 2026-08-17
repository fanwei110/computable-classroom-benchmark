import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 参数
K = 97.5
r = 0.043
T = 0.58
S_range = np.linspace(70, 140, 500)
volatility_params = [0.15, 0.276, 0.40]  # 可调

# 计算看涨期权 delta
def delta_call(S, K, r, T, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 绘制
plt.figure(figsize=(8, 5))
for sigma in volatility_params:
    delta_vals = delta_call(S_range, K, r, T, sigma)
    plt.plot(S_range, delta_vals, label=f'σ = {sigma*100:.1f}%')

plt.axvline(x=K, color='gray', linestyle='--', alpha=0.5)
plt.xlabel('标的价格')
plt.ylabel('Delta')
plt.title('看涨期权 Delta 随标的价格变化')
plt.legend()
plt.grid(True)

# 保存图片
fig_path = 'delta_vs_spot.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# 计算特定点：S=110, σ=27.6%
S_specific = 110
sigma_specific = 0.276
delta_val = delta_call(S_specific, K, r, T, sigma_specific)

# 结果字典
result = {
    'delta_at_s110': round(delta_val, 6),
    'figure_path': fig_path
}
print(result)
