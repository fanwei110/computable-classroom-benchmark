import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ========== 可调参数 ==========
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余期限（年）
S_range = np.linspace(70, 140, 300)  # 标的价格区间
sigmas = [0.15, 0.276, 0.40]         # 波动率列表
target_S = 110
target_sigma = 0.276
# ==============================

def bs_delta(S, K, r, T, sigma):
    """计算看涨期权的Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 绘图
plt.figure(figsize=(10, 6))
for sigma in sigmas:
    delta = bs_delta(S_range, K, r, T, sigma)
    plt.plot(S_range, delta, label=f'σ = {sigma*100:.1f}%')

plt.axvline(K, color='gray', linestyle='--', alpha=0.7, label=f'Strike = {K}')
plt.xlabel('Spot Price')
plt.ylabel('Delta')
plt.title('Call Option Delta vs Spot Price')
plt.legend()
plt.grid(True)

# 保存图片
fig_path = 'delta_vs_spot.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# 计算指定点的Delta
delta_at_s110 = bs_delta(target_S, K, r, T, target_sigma)

# 按要求存入字典
result = {
    'delta_at_s110': round(delta_at_s110, 6),  # 保留6位小数
    'figure_path': fig_path
}

# 输出结果（模拟实际运行时的输出）
print(result)
