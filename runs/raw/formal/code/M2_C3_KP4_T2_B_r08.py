import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# 参数
K = 97.5
r = 0.043
T = 0.58
vols = [0.15, 0.276, 0.40]
S_range = np.linspace(70, 140, 300)

# 计算 d1 和 Delta
def delta(S, vol):
    d1 = (np.log(S/K) + (r + vol**2 / 2) * T) / (vol * np.sqrt(T))
    return norm.cdf(d1)

# 绘图
plt.figure(figsize=(8, 5))
for vol in vols:
    d = delta(S_range, vol)
    plt.plot(S_range, d, label=f'Vol = {vol*100:.1f}%')
plt.axvline(x=110, color='gray', linestyle='--', alpha=0.7)
plt.axhline(y=0.5, color='black', linestyle=':', alpha=0.5)
plt.xlabel('Spot Price')
plt.ylabel('Delta')
plt.title('Call Option Delta Curve (K=97.5, r=4.3%, T=0.58)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图片
fig_path = 'delta_curve.png'
plt.savefig(fig_path, dpi=150)
plt.close()

# 计算 S=110, vol=27.6% 的 Delta
S_target = 110
vol_target = 0.276
delta_target = delta(S_target, vol_target)

# 构造结果字典
result = {
    'delta_at_s110': delta_target,
    'figure_path': os.path.abspath(fig_path)
}

print(result)
