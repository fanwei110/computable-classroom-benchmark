import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ================= 1. 参数与数据定义 =================
# 初始无风险利率与市场收益率（采用小数形式参与计算）
rf_init = 2.3  # 百分比形式，用于滑块初始值
rm_init = 9.4  # 百分比形式，用于滑块初始值

rf = rf_init / 100.0
rm = rm_init / 100.0

# Beta范围与SML上的点
beta_range = np.linspace(0, 2, 100)
sml_y = (rf + beta_range * (rm - rf)) * 100

# 股票数据点：X, Y, Z (Beta, 收益率%)
stocks = {
    'X': (0.62, 8.1),
    'Y': (1.18, 13.1),
    'Z': (1.51, 9.9)
}

# ================= 2. 绘图初始化 =================
# 处理中文字体显示，适应课堂投屏环境
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25)  # 留出底部空间给滑块

# 画SML初始线
line_sml, = ax.plot(beta_range, sml_y, 'b-', lw=2.5, label='SML (证券市场线)')

# 画Alpha指示虚线（偏离SML的部分）并标记三个股票点
vlines = []  # 存储垂直虚线对象，方便后续滑块更新
for label, (b, r) in stocks.items():
    er_sml = (rf + b * (rm - rf)) * 100
    # 画从SML理论值到实际值的虚线（直观展示Alpha）
    vl, = ax.plot([b, b], [er_sml, r], color='gray', linestyle='--', alpha=0.7)
    vlines.append((vl, b, r))
    # 画股票散点
    ax.scatter(b, r, color='red', s=80, zorder=5)
    # 标注文本
    x_offset = 5 if r >= er_sml else 5
    y_offset = 5 if r >= er_sml else -15
    ax.annotate(f'{label} ({b}, {r}%)', xy=(b, r), xytext=(x_offset, y_offset),
                textcoords='offset points', fontsize=11, weight='bold')

# 在图上显示斜率与Beta=1.27的收益信息（随滑块更新）
sml_slope = rm - rf
er_at_beta_127 = rf + 1.27 * sml_slope
info_text = ax.text(0.02, 0.95, f'SML斜率(市场风险溢价): {sml_slope*100:.2f}%\nBeta=1.27 期望收益: {er_at_beta_127*100:.2f}%',
                    transform=ax.transAxes, fontsize=12, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# 标记无风险利率点和市场组合点
ax.scatter(0, rf * 100, color='green', s=80, zorder=5, label=f'无风险利率 ({rf_init}%)')
ax.scatter(1, rm * 100, color='orange', s=80, zorder=5, label=f'市场组合 M ({rm_init}%)')

# 坐标轴与格式设置
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('期望收益率 (%)', fontsize=12)
ax.set_title('CAPM 与证券市场线 (SML)', fontsize=15, weight='bold')
ax.set_xlim(0, 2)
ax.set_ylim(-1, 20)  # 给定初始范围，滑块拉大时可能超出，但初始展示完美
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(loc='lower right', fontsize=10)

# ================= 3. 交互式滑块 =================
# 调整颜色与位置
axcolor = 'lightgoldenrodyellow'
ax_rf_slider = plt.axes([0.15, 0.10, 0.75, 0.03], facecolor=axcolor)
ax_rm_slider = plt.axes([0.15, 0.15, 0.75, 0.03], facecolor=axcolor)

slider_rf = Slider(ax_rf_slider, '无风险利率 (%)', 0.0, 10.0, valinit=rf_init, valstep=0.1)
slider_rm = Slider(ax_rm_slider, '市场收益 (%)', 0.0, 20.0, valinit=rm_init, valstep=0.1)

# 定义滑块更新函数
def update(val):
    rf_new = slider_rf.val / 100.0
    rm_new = slider_rm.val / 100.0
    
    # 更新SML线
    sml_y_new = (rf_new + beta_range * (rm_new - rf_new)) * 100
    line_sml.set_ydata(sml_y_new)
    
    # 更新Alpha指示虚线
    for vl, b, r in vlines:
        er_sml_new = (rf_new + b * (rm_new - rf_new)) * 100
        vl.set_ydata([er_sml_new, r])
        
    # 更新图上文本信息
    new_slope = rm_new - rf_new
    new_er = rf_new + 1.27 * new_slope
    info_text.set_text(f'SML斜率(市场风险溢价): {new_slope*100:.2f}%\nBeta=1.27 期望收益: {new_er*100:.2f}%')
    
    # 重绘图形
    fig.canvas.draw_idle()

# 绑定滑块事件
slider_rf.on_changed(update)
slider_rm.on_changed(update)

# ================= 4. 计算结果存储与图形保存 =================
# 保存初始状态下的图形
figure_path = 'sml_plot.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')

# 弹出交互式窗口供课堂拖动演示
plt.show()

# 按照输出契约存入字典（保留4位小数以兼顾精确度）
result = {
    'sml_slope': round(sml_slope, 4),
    'er_at_beta_127': round(er_at_beta_127, 4),
    'figure_path': figure_path
}

# 控制台输出供教师核对
print("运行结果存入 result 字典：")
print(result)
