import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from matplotlib.widgets import Slider

# 计算约定与参数
K = 97.5
r = 0.043
T = 0.58
S = np.linspace(70, 140, 500)
initial_sigmas = [0.15, 0.276, 0.40]

# Black-Scholes 看涨期权 Delta 计算函数
def bs_call_delta(S, K, r, T, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    return norm.cdf(d1)

# 计算标的等于110、波动率27.6%时的Delta
delta_s110 = bs_call_delta(110, K, r, T, 0.276)

# 绘图准备
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.35)  # 为底部滑块留出空间

lines = []
for sigma in initial_sigmas:
    delta = bs_call_delta(S, K, r, T, sigma)
    line, = ax.plot(S, delta, label=f'σ = {sigma*100:.1f}%')
    lines.append(line)

ax.set_xlabel('Underlying Price (S)')
ax.set_ylabel('Call Delta')
ax.set_title('Delta vs. Underlying Price (K=97.5, r=4.3%, T=0.58yr)')
ax.legend(loc='upper left')
ax.grid(True)

# 添加波动率可调滑块
ax_sigma1 = plt.axes([0.15, 0.20, 0.7, 0.03])
ax_sigma2 = plt.axes([0.15, 0.15, 0.7, 0.03])
ax_sigma3 = plt.axes([0.15, 0.10, 0.7, 0.03])

slider1 = Slider(ax_sigma1, 'Vol 1 (%)', 1, 100, valinit=initial_sigmas[0]*100)
slider2 = Slider(ax_sigma2, 'Vol 2 (%)', 1, 100, valinit=initial_sigmas[1]*100)
slider3 = Slider(ax_sigma3, 'Vol 3 (%)', 1, 100, valinit=initial_sigmas[2]*100)

def update(val):
    for i, slider in enumerate([slider1, slider2, slider3]):
        sigma = slider.val / 100
        lines[i].set_ydata(bs_call_delta(S, K, r, T, sigma))
        lines[i].set_label(f'σ = {sigma*100:.1f}%')
    ax.legend(loc='upper left')
    fig.canvas.draw_idle()

slider1.on_changed(update)
slider2.on_changed(update)
slider3.on_changed(update)

# 保存图像
figure_path = 'delta_plot.png'
fig.savefig(figure_path, dpi=150)

# 构建输出字典
result = {
    'delta_at_s110': round(float(delta_s110), 6),
    'figure_path': figure_path
}

print(result)
