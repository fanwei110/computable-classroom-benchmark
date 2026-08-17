import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ========== 可调参数 ==========
K = 97.5          # 行权价
r = 0.043         # 无风险利率（连续复利）
T = 0.58          # 剩余年限
S_range = np.linspace(70, 140, 300)  # 标的价格范围
sigmas = [0.15, 0.276, 0.40]         # 波动率参数（可调）
S_target = 110
sigma_target = 0.276
# ==============================

def delta_call(S, K, r, T, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 计算指定点的 Delta
delta_s110 = delta_call(S_target, K, r, T, sigma_target)

# 画图
plt.figure(figsize=(8, 5))
for sigma in sigmas:
    deltas = delta_call(S_range, K, r, T, sigma)
    plt.plot(S_range, deltas, label=f'σ = {sigma*100:.1f}%')

plt.axhline(0.5, color='grey', linestyle='--', linewidth=0.8)
plt.axvline(K, color='grey', linestyle='--', linewidth=0.8)
plt.xlabel('Spot Price')
plt.ylabel('Delta')
plt.title('Call Option Delta vs Spot Price')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
fig_path = 'delta_vs_spot.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# 结果字典
result = {
    'delta_at_s110': round(delta_s110, 6),
    'figure_path': fig_path
}

print(result)
