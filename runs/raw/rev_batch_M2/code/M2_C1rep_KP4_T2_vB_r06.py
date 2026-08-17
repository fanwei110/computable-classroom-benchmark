import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

def calculate_delta(S, K, r, T, sigma):
    """计算看涨期权的delta"""
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

# 参数设置
K = 97.5  # 行权价
r = 0.043  # 无风险利率
T = 0.58  # 到期时间
S_range = np.linspace(70, 140, 1000)  # 标的资产价格范围
vols = [0.15, 0.276, 0.40]  # 三个波动率
vol_labels = ['15%', '27.6%', '40%']

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))

# 计算并绘制三条delta曲线
for vol, label in zip(vols, vol_labels):
    delta_values = calculate_delta(S_range, K, r, T, vol)
    ax.plot(S_range, delta_values, linewidth=2, label=f'Vol = {label}')

# 计算特定点的delta值
S_specific = 110
vol_specific = 0.276
delta_at_s110 = calculate_delta(S_specific, K, r, T, vol_specific)

# 在图上标注特定点
ax.scatter(S_specific, delta_at_s110, color='red', s=100, zorder=5)
ax.annotate(f'Delta = {delta_at_s110:.4f}\n(S=110, Vol=27.6%)', 
            xy=(S_specific, delta_at_s110), 
            xytext=(S_specific+10, delta_at_s110-0.1),
            arrowprops=dict(arrowstyle='->', color='red'),
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
            fontsize=10)

# 图表设置
ax.set_xlabel('标的资产价格 (S)', fontsize=12)
ax.set_ylabel('Delta', fontsize=12)
ax.set_title('Delta曲线对比 (K=97.5, r=4.3%, T=0.58)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left', fontsize=10)
ax.set_xlim(70, 140)
ax.set_ylim(0, 1.05)

# 添加水平参考线
ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5)
ax.axhline(y=0, color='black', linewidth=0.5)
ax.axvline(x=K, color='gray', linestyle='--', alpha=0.3, label=f'行权价 K={K}')

# 保存图表
output_dir = os.getcwd()
figure_path = os.path.join(output_dir, 'delta_curves.png')
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 创建结果字典
result = {
    'delta_at_s110': round(delta_at_s110, 4),
    'figure_path': figure_path
}

print(f"S=110, Vol=27.6%时的Delta值: {result['delta_at_s110']}")
print(f"图表已保存至: {result['figure_path']}")
