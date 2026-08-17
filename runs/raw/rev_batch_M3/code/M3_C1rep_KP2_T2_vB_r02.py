import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# 初始参数
rf_init = 2.3
rm_init = 9.4

# 计算要求的数值结果
sml_slope = rm_init - rf_init
er_at_beta_127 = rf_init + 1.27 * sml_slope

# 创建画布与子图，调整底部预留滑块空间
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25)

# 画SML初始线
beta_vals = np.linspace(0, 2, 100)
sml_line, = ax.plot(beta_vals, rf_init + beta_vals * (rm_init - rf_init), 'b-', lw=2, label='SML')

# 标出三个点 X, Y, Z
ax.scatter([0.62, 1.18, 1.51], [8.1, 13.1, 9.9], color=['red', 'green', 'purple'], zorder=5)
ax.annotate('X (0.62, 8.1%)', xy=(0.62, 8.1), xytext=(0.62+0.05, 8.1+0.8), color='red')
ax.annotate('Y (1.18, 13.1%)', xy=(1.18, 13.1), xytext=(1.18+0.05, 13.1+0.8), color='green')
ax.annotate('Z (1.51, 9.9%)', xy=(1.51, 9.9), xytext=(1.51+0.05, 9.9+0.8), color='purple')

# 设置图表格式
ax.set_xlabel('Beta')
ax.set_ylabel('Expected Return (%)')
ax.set_title('Security Market Line (SML)')
ax.legend()
ax.grid(True)
ax.set_xlim(0, 2)
ax.set_ylim(0, 20)

# 添加滑块轴
ax_rf = plt.axes([0.15, 0.1, 0.7, 0.03])
ax_rm = plt.axes([0.15, 0.05, 0.7, 0.03])

# 创建滑块
s_rf = Slider(ax_rf, 'Rf (%)', 0.0, 10.0, valinit=rf_init)
s_rm = Slider(ax_rm, 'Rm (%)', 0.0, 20.0, valinit=rm_init)

# 滑块更新函数
def update(val):
    rf = s_rf.val
    rm = s_rm.val
    sml_line.set_ydata(rf + beta_vals * (rm - rf))
    fig.canvas.draw_idle()

s_rf.on_changed(update)
s_rm.on_changed(update)

# 保存图表
figure_path = 'sml_plot.png'
plt.savefig(figure_path)

# 构建输出字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 打印结果以供检查
print(result)
