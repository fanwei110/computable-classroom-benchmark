import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 初始参数（百分比）
rf_init = 2.3
rm_init = 9.4

# 计算市场风险溢价（SML 斜率）和 beta=1.27 处的期望收益
sml_slope = rm_init - rf_init                 # 7.1
er_at_beta_127 = rf_init + 1.27 * sml_slope    # 11.317

# 创建图形，留出底部空间放置滑块
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.25)

# 生成 beta 轴数据
beta = np.linspace(0, 2, 200)

# 初始 SML 线
er_sml = rf_init + beta * sml_slope
line, = ax.plot(beta, er_sml, 'b-', linewidth=2, label='SML')

# 三只股票的点
stocks_beta = [0.62, 1.18, 1.51]
stocks_er   = [8.1, 13.1, 9.9]
ax.scatter(stocks_beta, stocks_er, color='red', s=50, zorder=5, label='Stocks')

# 添加标签
ax.text(0.62, 8.1, 'X', fontsize=11, ha='right', va='bottom')
ax.text(1.18, 13.1, 'Y', fontsize=11, ha='left', va='bottom')
ax.text(1.51, 9.9, 'Z', fontsize=11, ha='left', va='top')

# 坐标轴与标题
ax.set_xlabel('Beta')
ax.set_ylabel('Expected Return (%)')
ax.set_title('Security Market Line (SML)')
ax.set_xlim(0, 2)
ax.set_ylim(0, 20)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend()

# 滑块轴
ax_rf = plt.axes([0.2, 0.12, 0.65, 0.03])
ax_rm = plt.axes([0.2, 0.06, 0.65, 0.03])

# 创建滑块
slider_rf = Slider(ax_rf, 'Risk-free rate (%)', 0.0, 5.0,
                   valinit=rf_init, valstep=0.1)
slider_rm = Slider(ax_rm, 'Market return (%)', 5.0, 15.0,
                   valinit=rm_init, valstep=0.1)

# 更新函数：滑块值改变时重新计算 SML 线
def update(val):
    rf = slider_rf.val
    rm = slider_rm.val
    slope = rm - rf
    line.set_ydata(rf + beta * slope)
    fig.canvas.draw_idle()

slider_rf.on_changed(update)
slider_rm.on_changed(update)

# 保存图形（初始状态）
figure_path = 'sml_plot.png'
fig.savefig(figure_path, dpi=150)

# 显示交互窗口
plt.show()

# 按要求输出结果
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 打印以便查看
print(result)
