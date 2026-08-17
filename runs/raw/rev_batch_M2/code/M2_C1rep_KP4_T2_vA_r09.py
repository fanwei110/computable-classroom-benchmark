import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import math

# ========== 可调参数 ==========
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余年限
S_range = np.linspace(70, 140, 500)  # 标的价格范围
volatilities = [0.15, 0.276, 0.40]   # 波动率参数（可手动调整）
S_target = 110    # 需要报 delta 的标的价格
sigma_target = 0.276  # 对应的波动率
# =============================

def call_delta(S, K, r, T, sigma):
    """计算欧式看涨期权的 delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 画图
plt.figure(figsize=(10, 6))
for sigma in volatilities:
    delta = call_delta(S_range, K, r, T, sigma)
    plt.plot(S_range, delta, label=f'σ = {sigma*100:.1f}%')

plt.axvline(K, color='gray', linestyle='--', alpha=0.6, label=f'Strike = {K}')
plt.xlabel('Spot Price')
plt.ylabel('Delta')
plt.title('Call Delta vs Spot Price')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
figure_path = 'delta_vs_S.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')

# 计算指定点的 delta
delta_target = call_delta(S_target, K, r, T, sigma_target)
print(f"Delta at S={S_target}, σ={sigma_target*100:.1f}%: {delta_target:.6f}")

# 存入结果字典
result = {
    'delta_at_s110': delta_target,
    'figure_path': figure_path
}

print("\nresult dictionary:")
print(result)
