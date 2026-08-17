import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

# --- 1. 计算部分 ---
rf = 0.023
rm = 0.094

# SML斜率即为市场风险溢价
sml_slope = rm - rf  # 0.094 - 0.023 = 0.071

# 计算beta为1.27时的预期收益率
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope  # 0.023 + 1.27 * 0.071 = 0.11317

# --- 2. 绘图部分 ---
fig, ax = plt.subplots(figsize=(10, 8))
plt.subplots_adjust(bottom=0.25)

# SML线的数据
betas = np.linspace(0, 2, 100)
sml_line, = ax.plot(betas, rf + betas * sml_slope, 'b-', lw=2, label='SML')

# 标注点 X, Y, Z
pts_beta = [0.62, 1.18, 1.51]
pts_ret = [0.081, 0.131, 0.099]
pts_names = ['X', 'Y', 'Z']
ax.scatter(pts_beta, pts_ret, color='red', zorder=5, label='Assets (X, Y, Z)')
for i in range(3):
    ax.annotate(f'{pts_names[i]} ({pts_beta[i]}, {pts_ret[i]*100:.1f}%)',
                (pts_beta[i], pts_ret[i]),
                textcoords="offset points", xytext=(10,10), ha='left')

# 标注初始的 rf 和 rm 的点
rf_point, = ax.plot(0, rf, 'go', markersize=10, label='$r_f$')
rm_point, = ax.plot(1, rm, 'go', markersize=10, label='$E(r_m)$')

# 设置坐标轴
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.20)
ax.set_xlabel('Beta ($\\beta$)')
ax.set_ylabel('Expected Return ($E(r)$)')
ax.set_title('Security Market Line (SML)')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))

# 添加滑动条（使其成为“可拖动”的交互控件）
ax_rf_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
ax_rm_slider = plt.axes([0.2, 0.15, 0.65, 0.03])

slider_rf = Slider(ax_rf_slider, 'Risk-free Rate ($r_f$)', 0.0, 0.1, valinit=rf, valstep=0.001)
slider_rm = Slider(ax_rm_slider, 'Market Return ($E(r_m)$)', 0.0, 0.2, valinit=rm, valstep=0.001)

# 滑动条回调函数：拖动时更新SML线和rf/rm标记点
def update(val):
    current_rf = slider_rf.val
    current_rm = slider_rm.val
    current_slope = current_rm - current_rf
    sml_line.set_ydata(current_rf + betas * current_slope)
    rf_point.set_ydata([current_rf])
    rm_point.set_ydata([current_rm])
    fig.canvas.draw_idle()

slider_rf.on_changed(update)
slider_rm.on_changed(update)

# 保存图片
fig_path = 'sml_plot.png'
fig.savefig(fig_path)
plt.close(fig)

# --- 3. 结果输出 ---
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': fig_path
}

print(result)
