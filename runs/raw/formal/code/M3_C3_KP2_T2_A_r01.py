import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import matplotlib.ticker as mtick

# 1. 参数设置 (遵循小数表示约定)
rf = 0.023
rm = 0.094

# 2. 计算要求
sml_slope = rm - rf
er_at_beta_127 = rf + 1.27 * sml_slope

# 3. 绘制SML图
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25) # 为底部滑块留出空间

# SML线数据
beta_range = np.linspace(0, 2, 100)
er_range = rf + beta_range * sml_slope
line, = ax.plot(beta_range, er_range, label='SML', color='blue', linewidth=2)

# 标出X, Y, Z三个点
points = {'X': (0.62, 0.081), 'Y': (1.18, 0.131), 'Z': (1.51, 0.099)}
for name, (b, er) in points.items():
    ax.scatter(b, er, zorder=5, label=f'{name} ($\\beta$={b}, E[R]={er:.1%})')
    ax.annotate(f'{name}\n({b}, {er:.1%})', (b, er), textcoords="offset points", xytext=(10,5), ha='left')

# 标出beta=1.27对应的期望收益点
ax.scatter(1.27, er_at_beta_127, color='red', marker='x', s=100, zorder=5, 
           label=f'$\\beta=1.27$ (E[R]={er_at_beta_127:.2%})')

# 图表格式设置
ax.set_xlabel('Beta ($\\beta$)', fontsize=12)
ax.set_ylabel('Expected Return (E[R])', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=1))
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.20)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left')

# 4. 添加交互式Slider (满足上课调参数需求)
ax_rf = plt.axes([0.15, 0.1, 0.75, 0.03])
ax_rm = plt.axes([0.15, 0.05, 0.75, 0.03])

slider_rf = Slider(ax_rf, 'Risk-free ($r_f$)', 0.0, 0.10, valinit=rf, valstep=0.001)
slider_rm = Slider(ax_rm, 'Market ($E[R_m]$)', 0.0, 0.25, valinit=rm, valstep=0.001)

def update(val):
    rf_new = slider_rf.val
    rm_new = slider_rm.val
    new_slope = rm_new - rf_new
    new_er_range = rf_new + beta_range * new_slope
    line.set_ydata(new_er_range)
    fig.canvas.draw_idle()

slider_rf.on_changed(update)
slider_rm.on_changed(update)

# 5. 保存图像
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')

# 上课时请取消下行注释，即可通过弹窗拖动滑块调参
# plt.show() 

# 6. 按照输出契约存入字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

print(result)
