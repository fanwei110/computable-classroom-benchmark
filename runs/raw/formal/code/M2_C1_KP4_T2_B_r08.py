import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# ---------- 参数设置 ----------
K = 97.5
r = 0.043
T = 0.58
S_range = np.linspace(70, 140, 500)
vols = [0.15, 0.276, 0.40]

# ---------- 计算Delta ----------
def delta_call(S, K, r, T, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 指定点的Delta
S_target = 110
vol_target = 0.276
delta_target = delta_call(S_target, K, r, T, vol_target)

# ---------- 绘图 ----------
plt.figure(figsize=(10, 6))
for vol in vols:
    delta = delta_call(S_range, K, r, T, vol)
    plt.plot(S_range, delta, label=f'σ = {vol*100:.1f}%')

plt.axvline(S_target, color='gray', linestyle='--', linewidth=0.8)
plt.axhline(delta_target, color='gray', linestyle='--', linewidth=0.8)
plt.scatter(S_target, delta_target, color='red', zorder=5)
plt.text(S_target + 0.5, delta_target, f'({S_target}, {delta_target:.4f})',
         fontsize=10, color='red')

plt.xlabel('标的资产价格')
plt.ylabel('Delta')
plt.title('看涨期权 Delta 曲线')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ---------- 结果存入字典 ----------
result = {
    'delta_at_s110': round(delta_target, 6),
    'figure_path': figure_path
}

# 输出
print(result)
