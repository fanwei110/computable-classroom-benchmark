import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# 设置中文字体，防止图表中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ---------------- 参数设置 ----------------
K = 97.5          # 行权价
r = 0.043         # 无风险利率 4.3%
T = 0.58          # 到期时间
S_range = np.linspace(70, 140, 400)  # 标的资产价格范围
vols = [0.15, 0.276, 0.40]           # 波动率列表（可调）

# ---------------- Delta计算函数 ----------------
def call_delta(S, K, r, T, vol):
    """计算欧式看涨期权的Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    return norm.cdf(d1)

# ---------------- 计算特定值：标的110，vol 27.6% ----------------
specific_S = 110
specific_vol = 0.276
delta_s110 = call_delta(specific_S, K, r, T, specific_vol)

# ---------------- 绘制Delta曲线 ----------------
plt.figure(figsize=(10, 6))

for vol in vols:
    deltas = call_delta(S_range, K, r, T, vol)
    plt.plot(S_range, deltas, label=f'Vol = {vol*100:.1f}%')

# 标出特定计算点
plt.scatter([specific_S], [delta_s110], color='red', zorder=5)
plt.annotate(f'S=110, Vol=27.6%\nDelta={delta_s110:.4f}', 
             xy=(specific_S, delta_s110), 
             xytext=(specific_S+5, delta_s110-0.15),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headlength=4),
             fontsize=10)

plt.title(f'看涨期权Delta曲线 (K={K}, r={r*100}%, T={T})')
plt.xlabel('标的资产价格 (S)')
plt.ylabel('Delta')
plt.legend(title="波动率(可调)")
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图片
figure_path = 'delta_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ---------------- 构建输出结果 ----------------
result = {
    'delta_at_s110': delta_s110,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
