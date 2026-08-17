import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def bs_call_delta(S, K, r, T, vol):
    """
    计算欧式看涨期权的 Delta (Black-Scholes 闭式解)
    S: 标的资产价格 (可以是标量或数组)
    K: 行权价
    r: 无风险利率
    T: 到期期限 (年)
    vol: 波动率
    """
    d1 = (np.log(S / K) + (r + 0.5 * vol**2) * T) / (vol * np.sqrt(T))
    return norm.cdf(d1)

# ================= 基础参数 =================
K = 97.5
r = 0.043
T = 0.58

# 标的资产价格网格 (70 到 140)
S_grid = np.linspace(70, 140, 500)

# 三条曲线的波动率参数
vols = [0.15, 0.276, 0.40]

# ================= 特定点的 Delta 计算 =================
S_target = 110
vol_target = 0.276
delta_at_s110 = bs_call_delta(S_target, K, r, T, vol_target)

# ================= 绘图 =================
plt.figure(figsize=(10, 6))

# 遍历波动率，计算并绘制三条 Delta 曲线
for vol in vols:
    deltas = bs_call_delta(S_grid, K, r, T, vol)
    plt.plot(S_grid, deltas, linewidth=2, label=f'vol = {vol*100:.1f}%')

# 在图上标出标的110、vol 27.6% 的 delta 点，增加投屏演示效果
plt.scatter([S_target], [delta_at_s110], color='red', s=60, zorder=5)
plt.annotate(f'S=110, vol=27.6%\nDelta={delta_at_s110:.4f}', 
             xy=(S_target, delta_at_s110), 
             xytext=(15, -15), 
             textcoords='offset points',
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
             fontsize=10,
             bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.8))

plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(K, color='grey', linestyle='--', linewidth=0.8, label=f'Strike K={K}')
plt.xlabel('Underlying Price (S)', fontsize=12)
plt.ylabel('Delta', fontsize=12)
plt.title('European Call Option Delta vs. Underlying Price (K=97.5, r=4.3%, T=0.58)', fontsize=14)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)

# ================= 保存图形 =================
figure_path = 'delta_curves.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 填充 Result =================
result = {
    'delta_at_s110': delta_at_s110,
    'figure_path': figure_path
}

# 教师投屏用，直接打印结果供确认
print(f"标的110、波动率27.6%的Delta值为: {result['delta_at_s110']:.6f}")
print(f"图形已保存至: {result['figure_path']}")
