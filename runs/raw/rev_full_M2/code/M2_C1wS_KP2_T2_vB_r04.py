import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 初始参数
rf0 = 0.023       # 无风险利率 2.3%
rm0 = 0.094       # 市场期望收益 9.4%
beta_vals = np.linspace(0, 2, 200)

# 三只股票 (beta, 期望收益)
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# 创建图形和轴
fig, ax = plt.subplots(figsize=(9, 6))
plt.subplots_adjust(bottom=0.25)   # 为滑块留出空间

# 初始 SML 线
er_sml = rf0 + beta_vals * (rm0 - rf0)
line_sml, = ax.plot(beta_vals, er_sml, 'b-', lw=2, label='SML')

# 无风险资产点 (β=0) 和市场组合点 (β=1)
point_rf, = ax.plot(0, rf0, 'ro', ms=8, label='RF (β=0)')
point_m,  = ax.plot(1, rm0, 'go', ms=8, label='Market (β=1)')

# 三只股票点
for name, (b, er) in stocks.items():
    ax.plot(b, er, 'kx', ms=10, zorder=5)
    ax.text(b, er, f'  {name}', fontsize=11, verticalalignment='bottom')

# 坐标轴标签、标题
ax.set_xlabel('Beta', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.20)
ax.legend(loc='upper left')
ax.grid(True, linestyle='--', alpha=0.6)

# 显示当前斜率与 β=1.27 期望收益的文本
slope_init = rm0 - rf0
er_127_init = rf0 + 1.27 * slope_init
text_slope = ax.text(1.55, 0.18, f'Slope = {slope_init:.4f}', fontsize=12,
                     bbox=dict(facecolor='white', alpha=0.8))
text_er    = ax.text(1.55, 0.16, f'E(R) at β=1.27 = {er_127_init:.4f}', fontsize=12,
                     bbox=dict(facecolor='white', alpha=0.8))

# 创建滑块：无风险利率 & 市场收益
ax_rf = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_rm = plt.axes([0.2, 0.10, 0.6, 0.03])
slider_rf = Slider(ax_rf, 'RF', 0.0, 0.05, valinit=rf0, valstep=0.001)
slider_rm = Slider(ax_rm, 'Market Return', 0.06, 0.15, valinit=rm0, valstep=0.001)

# 更新函数：拖动滑块时重新计算
def update(val):
    rf = slider_rf.val
    rm = slider_rm.val
    slope = rm - rf
    # 更新 SML 线
    line_sml.set_ydata(rf + beta_vals * slope)
    # 更新 rf 与市场组合点
    point_rf.set_ydata([rf])
    point_m.set_ydata([rm])
    # 更新文本
    text_slope.set_text(f'Slope = {slope:.4f}')
    text_er.set_text(f'E(R) at β=1.27 = {rf + 1.27*slope:.4f}')
    fig.canvas.draw_idle()

slider_rf.on_changed(update)
slider_rm.on_changed(update)

# 保存图形（初始状态）
figure_path = 'sml_demo.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')

# 显示交互窗口
plt.show()

# 输出要求的字典
result = {
    'sml_slope': slope_init,           # 0.071
    'er_at_beta_127': er_127_init,     # 0.11317
    'figure_path': figure_path
}
print(result)
