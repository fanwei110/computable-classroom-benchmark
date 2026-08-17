import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

# 初始参数
rf_init = 2.3
mkt_init = 9.4
beta = np.linspace(0, 2, 200)

# 资产点
points = {'X': (0.62, 8.1), 'Y': (1.18, 13.1), 'Z': (1.51, 9.9)}

# 创建图形
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.3)
line, = ax.plot(beta, rf_init + beta * (mkt_init - rf_init), 'k-', lw=2, label='SML')
mkt_point, = ax.plot(1, mkt_init, 'bo', markersize=10, label='Market')
asset_plots = []
for name, (b, er) in points.items():
    p, = ax.plot(b, er, 'ro', markersize=8)
    ax.text(b, er, name, fontsize=9, ha='right')
    asset_plots.append(p)

ax.set_xlim(0, 2)
ax.set_ylim(0, 15)
ax.set_xlabel('Beta')
ax.set_ylabel('Expected Return (%)')
ax.set_title('Security Market Line')
ax.grid(True)
ax.axhline(rf_init, color='gray', linestyle='--', alpha=0.5)
ax.legend()

# 滑块轴
ax_rf = plt.axes([0.2, 0.15, 0.65, 0.03])
ax_mkt = plt.axes([0.2, 0.05, 0.65, 0.03])
slider_rf = Slider(ax_rf, 'rf (%)', 0.0, 5.0, valinit=rf_init, valstep=0.1)
slider_mkt = Slider(ax_mkt, 'Market (%)', 6.0, 12.0, valinit=mkt_init, valstep=0.1)

def update(val):
    rf = slider_rf.val
    mkt = slider_mkt.val
    line.set_ydata(rf + beta * (mkt - rf))
    mkt_point.set_ydata([mkt])
    ax.axhline(rf, color='gray', linestyle='--', alpha=0.5)
    fig.canvas.draw_idle()

slider_rf.on_changed(update)
slider_mkt.on_changed(update)

# 保存静态图片
fig_path = 'sml_plot.png'
plt.savefig(fig_path)
plt.show()

# 计算
sml_slope = mkt_init - rf_init
er_beta_127 = rf_init + 1.27 * sml_slope

result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_beta_127,
    'figure_path': fig_path
}
print(result)
