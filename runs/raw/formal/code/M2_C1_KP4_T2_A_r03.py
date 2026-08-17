import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ========== 可调参数 ==========
S_range = np.linspace(70, 140, 200)   # 标的价范围
K = 97.5                              # 行权价
r = 0.043                             # 无风险利率
T = 0.58                              # 剩余到期时间（年）
volatilities = [0.15, 0.276, 0.40]   # 波动率参数（可调）
# =============================

def delta_call(S, K, r, T, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    return norm.cdf(d1)

# 绘图
plt.figure(figsize=(10, 6))
for sigma in volatilities:
    delta_vals = delta_call(S_range, K, r, T, sigma)
    plt.plot(S_range, delta_vals, label=f'σ={sigma*100:.1f}%')

plt.axvline(x=K, color='gray', linestyle='--', alpha=0.5, label=f'K={K}')
plt.xlabel('Spot Price')
plt.ylabel('Delta')
plt.title('Call Option Delta vs Spot Price')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
figure_path = './delta_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 计算特定点：S=110, σ=27.6%
sigma_target = 0.276
S_target = 110
delta_at_s110 = delta_call(S_target, K, r, T, sigma_target)

# 按契约整理结果
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

print(result)
