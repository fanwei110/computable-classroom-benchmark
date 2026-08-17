import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import os

# 初始参数（以百分比表示）
rf_init = 2.3
rm_init = 9.4

# 需要标记的三个资产点
points = {'X': (0.62, 8.1), 'Y': (1.18, 13.1), 'Z': (1.51, 9.9)}

# 计算初始SML斜率和 Beta=1.27 时的预期收益
sml_slope = rm_init - rf_init  # 7.1 (%)
er_at_beta_127 = rf_init + 1.27 * sml_slope  # 11.317 (%)

# 创建图形和坐标轴，为底部滑块留出空间
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25)

# 生成Beta数据并绘制初始SML
beta_range = np.linspace(0, 2, 100)
sml_line, = ax.plot(beta_range, rf_init + beta_range * sml_slope, 'b-', lw=2, label='SML')

# 标记三个资产点 X, Y, Z
colors = {'X': 'red', 'Y': 'green', 'Z': 'purple'}
for label, (b, r) in points.items():
    ax.scatter(b, r, color=colors[label], zorder=5, label=f'{label} ({b}, {r}%)')
    ax.text(b + 0.03, r + 0.4, f'{label}({b}, {r}%)', fontsize=11, color=colors[label])

# 标记无风险资产(Rf)和市场组合(M)
ax.scatter(0, rf_init, color='black', zorder=5, label=f'Rf (0, {rf_init}%)')
ax.text(0.03, rf_init + 0.4, f'Rf(0, {rf_init}%)', fontsize=11, color='black')
ax.scatter(1, rm_init, color='orange', zorder=5, label=f'Market (1, {rm_init}%)')
ax.text(1.03, rm_init + 0.4, f'M(1, {rm_init}%)', fontsize=11, color='orange')

# 设置图表格式
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return (%)', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.set_xlim(0, 2)
ax.set_ylim(0, 16)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left')

# 定义滑块的位置和属性
ax_rf = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_rm = plt.axes([0.25, 0.05, 0.65, 0.03])

s_rf = Slider(ax_rf, 'Rf (%)', 0.0, 5.0, valinit=rf_init, valstep=0.1)
s_rm = Slider(ax_rm, 'E(Rm) (%)', 5.0, 15.0, valinit=rm_init, valstep=0.1)

# 滑块更新函数：拖动时实时改变SML斜率
def update(val):
    rf = s_rf.val
    rm = s_rm.val
    slope = rm - rf
    sml_line.set_ydata(rf + beta_range * slope)
    fig.canvas.draw_idle()

s_rf.on_changed(update)
s_rm.on_changed(update)

# 保存图片到本地
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')

# 按照输出契约构造结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
