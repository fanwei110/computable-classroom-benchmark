import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 参数设定
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 到期时间（年）
S_range = np.linspace(70, 140, 200)  # 标的资产价格区间
vols = [0.15, 0.276, 0.40]           # 三条波动率曲线
target_S = 110.0
target_vol = 0.276

def compute_delta(S, K, r, T, sigma):
    """计算欧式看涨期权的 Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# ----- 计算目标点的 Delta -----
delta_at_s110 = compute_delta(target_S, K, r, T, target_vol)
print(f"Delta at S=110, vol=27.6%: {delta_at_s110:.6f}")

# ----- 绘制 Delta 曲线 -----
plt.figure(figsize=(10, 6))
for vol in vols:
    deltas = compute_delta(S_range, K, r, T, vol)
    plt.plot(S_range, deltas, label=f'Vol = {vol*100:.1f}%')

plt.axvline(K, color='gray', linestyle='--', alpha=0.5, label=f'Strike = {K}')
plt.xlabel('Underlying Price')
plt.ylabel('Delta')
plt.title('Call Option Delta vs. Underlying Price')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ----- 按要求构造结果字典 -----
result = {
    'delta_at_s110': round(delta_at_s110, 6),  # 保留6位小数，可根据需要调整
    'figure_path': figure_path
}

print("结果字典：", result)
