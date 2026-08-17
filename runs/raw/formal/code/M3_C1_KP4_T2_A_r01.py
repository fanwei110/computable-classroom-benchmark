import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from scipy.stats import norm
import os

# ===================== 固定参数 =====================
K = 97.5          # 行权价
r = 0.043         # 无风险利率
T = 0.58          # 剩余期限（年）
S_range = np.linspace(70, 140, 700)  # 标的价格范围

# ===================== 可调波动率参数（初始值） =====================
init_vol1 = 15.0   # %
init_vol2 = 27.6   # %
init_vol3 = 40.0   # %

# ===================== Black-Scholes Call Delta =====================
def call_delta(S, K, r, sigma, T):
    """计算欧式看涨期权的 Delta"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# ===================== 绘图 =====================
fig, ax = plt.subplots(figsize=(11, 8))
plt.subplots_adjust(bottom=0.25)

colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# 初始三条 Delta 曲线
line1, = ax.plot(S_range, call_delta(S_range, K, r, init_vol1/100, T),
                 color=colors[0], linewidth=2.2, label=f'σ = {init_vol1}%')
line2, = ax.plot(S_range, call_delta(S_range, K, r, init_vol2/100, T),
                 color=colors[1], linewidth=2.2, label=f'σ = {init_vol2}%')
line3, = ax.plot(S_range, call_delta(S_range, K, r, init_vol3/100, T),
                 color=colors[2], linewidth=2.2, label=f'σ = {init_vol3}%')

# 参考线
ax.axhline(y=0, color='gray', linewidth=0.5, linestyle='--')
ax.axhline(y=1, color='gray', linewidth=0.5, linestyle='--')
ax.axvline(x=K, color='red', linewidth=0.8, linestyle=':', label=f'行权价 K = {K}')

# 标注 S=110, σ=27.6% 处的 Delta
delta_s110 = call_delta(110, K, r, 0.276, T)
point_marker, = ax.plot(110, delta_s110, 'ko', markersize=9, zorder=5)
annot = ax.annotate(f'S=110, σ=27.6%\nΔ = {delta_s110:.4f}',
                    xy=(110, delta_s110),
                    xytext=(118, delta_s110 - 0.15),
                    fontsize=10, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color='black', lw=1.2),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gray'))

ax.set_xlabel('标的价格 (S)', fontsize=13)
ax.set_ylabel('Delta', fontsize=13)
ax.set_title('看涨期权 Delta 随标的价格变化\n(K = 97.5,  r = 4.3%,  T = 0.58 年)', fontsize=14)
ax.legend(fontsize=11, loc='upper left')
ax.set_xlim(70, 140)
ax.set_ylim(-0.05, 1.05)
ax.grid(True, alpha=0.3)

# ===================== 波动率滑块（可调参数） =====================
ax_vol1 = plt.axes([0.15, 0.15, 0.70, 0.025])
ax_vol2 = plt.axes([0.15, 0.10, 0.70, 0.025])
ax_vol3 = plt.axes([0.15, 0.05, 0.70, 0.025])

slider1 = Slider(ax_vol1, 'σ₁ (%)', 1, 80, valinit=init_vol1, valstep=0.1, color=colors[0])
slider2 = Slider(ax_vol2, 'σ₂ (%)', 1, 80, valinit=init_vol2, valstep=0.1, color=colors[1])
slider3 = Slider(ax_vol3, 'σ₃ (%)', 1, 80, valinit=init_vol3, valstep=0.1, color=colors[2])

def update(val):
    v1, v2, v3 = slider1.val, slider2.val, slider3.val
    line1.set_ydata(call_delta(S_range, K, r, v1/100, T))
    line2.set_ydata(call_delta(S_range, K, r, v2/100, T))
    line3.set_ydata(call_delta(S_range, K, r, v3/100, T))
    line1.set_label(f'σ = {v1}%')
    line2.set_label(f'σ = {v2}%')
    line3.set_label(f'σ = {v3}%')
    ax.legend(fontsize=11, loc='upper left')
    fig.canvas.draw_idle()

slider1.on_changed(update)
slider2.on_changed(update)
slider3.on_changed(update)

# ===================== 保存图片 =====================
fig_path = os.path.join(os.getcwd(), 'delta_vs_price.png')
fig.savefig(fig_path, dpi=150, bbox_inches='tight')

# ===================== 输出结果 =====================
print(f"S=110, σ=27.6% 时的 Delta = {delta_s110:.6f}")
print(f"图片已保存至: {fig_path}")

result = {
    'delta_at_s110': delta_s110,
    'figure_path': fig_path
}

print(f"\nresult = {result}")
