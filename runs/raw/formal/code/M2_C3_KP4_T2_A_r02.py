import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ==================== 参数定义（可调） ====================
K = 97.5                 # 行权价
r_annual = 0.043         # 年复利报价的债券收益率
T = 0.58                 # 剩余年限（年）
S_vals = np.linspace(70, 140, 300)  # 标的价区间
volatility_list = [0.15, 0.276, 0.40]  # 波动率参数（可调）

# 将年复利转换为连续复利
r_cont = np.log(1 + r_annual)

# ==================== Black-Scholes 看涨 Delta ====================
def call_delta(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ==================== 计算指定点的 Delta ====================
S_target = 110
sigma_target = 0.276
delta_at_s110 = call_delta(S_target, K, T, r_cont, sigma_target)

# ==================== 画图 ====================
fig, ax = plt.subplots(figsize=(10, 6))
for sigma in volatility_list:
    delta_vals = call_delta(S_vals, K, T, r_cont, sigma)
    ax.plot(S_vals, delta_vals, label=f'σ = {sigma*100:.1f}%')

ax.axvline(x=K, color='gray', linestyle='--', alpha=0.7, label=f'K = {K}')
ax.set_xlabel('Spot Price')
ax.set_ylabel('Delta')
ax.set_title('Call Delta vs Spot Price for Different Volatilities')
ax.legend()
ax.grid(True, alpha=0.3)

# 保存图片
figure_path = os.path.join(os.getcwd(), 'delta_vs_spot.png')
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ==================== 结果输出 ====================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

print(result)
