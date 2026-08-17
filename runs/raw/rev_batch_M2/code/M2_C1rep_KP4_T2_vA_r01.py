import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ========== 可调参数 ==========
S_range = np.linspace(70, 140, 300)   # 标的价格范围
K = 97.5                              # 行权价
r = 0.043                             # 无风险利率
T = 0.58                              # 剩余年限
volatility_list = [0.15, 0.276, 0.40] # 波动率参数，可自行修改
S_target = 110                        # 要计算 delta 的特定标的价格
sigma_target = 0.276                  # 对应波动率 27.6%
# ================================

def delta_call(S, K, r, T, sigma):
    """欧式看涨期权的 Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 绘图
plt.figure(figsize=(10, 6))
for vol in volatility_list:
    delta_vals = delta_call(S_range, K, r, T, vol)
    plt.plot(S_range, delta_vals, label=f'σ = {vol*100:.1f}%')

plt.axvline(x=K, color='gray', linestyle='--', linewidth=1, label=f'Strike K={K}')
plt.xlabel('Spot Price')
plt.ylabel('Delta')
plt.title('Call Option Delta vs Spot Price')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

# 保存图片
fig_path = 'delta_plot.png'
plt.savefig(fig_path, dpi=150)
plt.close()

# 计算指定点的 delta
delta_at_s110 = delta_call(S_target, K, r, T, sigma_target)

# 按要求存入结果字典
result = {
    'delta_at_s110': round(delta_at_s110, 6),
    'figure_path': fig_path
}

print(result)
