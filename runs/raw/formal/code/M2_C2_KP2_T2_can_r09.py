import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ------------------------------
# 1. 初始参数与数据
# ------------------------------
rf_init = 0.023      # 无风险利率 2.3%
rm_init = 0.094      # 市场期望收益 9.4%
beta_target = 1.27   # 需要报告的特定 beta

# 三只股票的数据 (beta, 实际收益)
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# ------------------------------
# 2. 创建图形与初始元素
# ------------------------------
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.30)  # 为滑块留空间

# 固定的 beta 范围
beta_vals = np.linspace(0, 2, 200)

# 初始 SML 线
sml_line, = ax.plot(beta_vals, rf_init + beta_vals * (rm_init - rf_init),
                    'b-', lw=2, label='SML')

# 无风险资产点 (beta=0)
rf_point, = ax.plot(0, rf_init, 'ko', markersize=8, label='无风险资产')
# 市场组合点 (beta=1)
mkt_point, = ax.plot(1, rm_init, 'ks', markersize=8, label='市场组合')

# 三只股票的点与标注
stock_points = []
stock_labels = []
for name, (b, er) in stocks.items():
    pt, = ax.plot(b, er, 'ro', markersize=8)
    stock_points.append(pt)
    # 文本标注
    lbl = ax.annotate(f'{name}  (β={b:.2f}, E(R)={er:.2%})',
                      xy=(b, er), xytext=(10, 10),
                      textcoords='offset points',
                      fontsize=9, color='darkred',
                      bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.5))
    stock_labels.append(lbl)

# 显示斜率和特定 beta 处的期望收益的文本
slope_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                     fontsize=11, verticalalignment='top',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
er_target_text = ax.text(0.02, 0.88, '', transform=ax.transAxes,
                         fontsize=11, verticalalignment='top',
                         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

# 图表装饰
ax.set_xlabel('Beta (β)')
ax.set_ylabel('期望收益 E(R)')
ax.set_title('证券市场线 (SML) 与可调参数')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='lower right')
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.25)

# 将纵轴设置为百分比格式
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1%}'.format(y)))

# ------------------------------
# 3. 滑块（参数化无风险利率与市场收益）
# ------------------------------
axcolor = 'lightgoldenrodyellow'
ax_rf = plt.axes([0.20, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_rm = plt.axes([0.20, 0.10, 0.65, 0.03], facecolor=axcolor)

slider_rf = Slider(ax_rf, '无风险利率 Rf', 0.0, 0.15, valinit=rf_init, valfmt='%.3f')
slider_rm = Slider(ax_rm, '市场期望收益 Rm', 0.02, 0.25, valinit=rm_init, valfmt='%.3f')

# ------------------------------
# 4. 更新函数
# ------------------------------
def update(val):
    rf = slider_rf.val
    rm = slider_rm.val
    # 更新 SML 线
    sml_line.set_ydata(rf + beta_vals * (rm - rf))
    # 更新无风险资产与市场组合点
    rf_point.set_ydata([rf])
    mkt_point.set_ydata([rm])
    # 更新斜率文本
    slope = rm - rf
    slope_text.set_text(f'SML 斜率 = {slope:.4f} ({slope:.2%})')
    # 更新 beta=1.27 处的期望收益
    er_target = rf + beta_target * slope
    er_target_text.set_text(f'β={beta_target} 处的 CAPM 期望收益 = {er_target:.4f} ({er_target:.2%})')
    fig.canvas.draw_idle()

# 连接滑块
slider_rf.on_changed(update)
slider_rm.on_changed(update)

# 初始调用更新函数以显示文本
update(None)

# ------------------------------
# 5. 计算最终报告值（基于初始参数）
# ------------------------------
sml_slope = rm_init - rf_init
er_at_beta_127 = rf_init + beta_target * sml_slope

# 打印到控制台
print(f"SML 斜率: {sml_slope:.4f} ({sml_slope:.2%})")
print(f"β={beta_target} 处的 CAPM 期望收益: {er_at_beta_127:.4f} ({er_at_beta_127:.2%})")

# ------------------------------
# 6. 保存图形并填充结果字典
# ------------------------------
figure_path = "sml_plot.png"
fig.savefig(figure_path, dpi=150, bbox_inches='tight')

result = {
    'sml_slope': sml_slope,           # 斜率（小数形式）
    'er_at_beta_127': er_at_beta_127, # beta=1.27 的 CAPM 期望收益（小数）
    'figure_path': figure_path        # 图片文件路径
}

print("\n结果字典:", result)

# 展示交互式图形（若在支持的环境中）
plt.show()
