import numpy as np
import matplotlib
matplotlib.use('Agg')  # 非交互式后端，确保文件保存
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ============================================================
# 参数设定
# ============================================================
rf_init = 0.023   # 无风险利率 2.3%
erm_init = 0.094  # 市场预期收益 9.4%

# 三只股票数据
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099),
}

# 计算 SML 斜率 (市场风险溢价)
def compute_slope(rf, erm):
    return erm - rf

# 计算给定 beta 的期望收益
def sml_expected_return(beta, rf, erm):
    return rf + (erm - rf) * beta

# 初始斜率与 beta=1.27 处的期望收益
initial_slope = compute_slope(rf_init, erm_init)
er_127 = sml_expected_return(1.27, rf_init, erm_init)

# ============================================================
# 绘图与交互控件
# ============================================================
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(left=0.12, bottom=0.25, top=0.93)

# SML 线数据
beta = np.linspace(0, 2, 100)
sml_line, = ax.plot(beta, sml_expected_return(beta, rf_init, erm_init),
                    'b-', linewidth=2, label='SML')

# 市场组合点
market_point, = ax.plot([1.0], [erm_init], 'ko', markersize=10, label='Market')
# 无风险资产点
rf_point, = ax.plot([0.0], [rf_init], 'ko', markersize=10, label='Risk-free')

# 三只股票
colors = {'X': 'red', 'Y': 'green', 'Z': 'purple'}
scatter_stocks = {}
for name, (b, er) in stocks.items():
    scatter_stocks[name] = ax.scatter(b, er, color=colors[name], s=120,
                                      label=f'{name} (β={b}, E[R]={er*100:.1f}%)',
                                      zorder=5, edgecolors='black', linewidth=0.8)

# 标注 beta=1.27 的点
beta_127 = 1.27
scatter_127 = ax.scatter([beta_127], [er_127], color='orange', marker='D',
                         s=100, zorder=6, edgecolors='black', linewidth=1.0,
                         label=f'β=1.27, E[R]={er_127*100:.2f}%')

# 图例与标签
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Security Market Line (SML) with Interactive Sliders', fontsize=14)
ax.set_xlim(-0.05, 2.1)
ax.set_ylim(0.0, 0.22)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left', fontsize=9)

# 标注 y 轴为百分比格式
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.0f}%'))

# 添加文本信息框（动态更新）
text_str = (f"Slope (Market Risk Premium): {initial_slope*100:.2f}%\n"
            f"E[R] at β=1.27: {er_127*100:.2f}%")
info_text = ax.text(0.97, 0.05, text_str, transform=ax.transAxes,
                    fontsize=11, verticalalignment='bottom',
                    horizontalalignment='right',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 创建滑块轴
ax_rf = plt.axes([0.15, 0.12, 0.7, 0.03])
ax_erm = plt.axes([0.15, 0.06, 0.7, 0.03])

# 创建滑块
slider_rf = Slider(ax_rf, 'Risk-free rate', 0.0, 0.08, valinit=rf_init, valfmt='%1.3f')
slider_erm = Slider(ax_erm, 'Market E[R]', 0.07, 0.18, valinit=erm_init, valfmt='%1.3f')

# 更新函数
def update(val):
    rf = slider_rf.val
    erm = slider_erm.val

    # 更新 SML 线
    sml_line.set_ydata(sml_expected_return(beta, rf, erm))

    # 更新市场点
    market_point.set_data([1.0], [erm])

    # 更新无风险点
    rf_point.set_data([0.0], [rf])

    # 更新 beta=1.27 点
    er_127_new = sml_expected_return(1.27, rf, erm)
    scatter_127.set_offsets(np.array([[1.27, er_127_new]]))

    # 更新信息文本
    slope_new = compute_slope(rf, erm)
    text_str_new = (f"Slope (Market Risk Premium): {slope_new*100:.2f}%\n"
                    f"E[R] at β=1.27: {er_127_new*100:.2f}%")
    info_text.set_text(text_str_new)

    fig.canvas.draw_idle()

slider_rf.on_changed(update)
slider_erm.on_changed(update)

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')

# ============================================================
# 输出结果字典
# ============================================================
result = {
    'sml_slope': initial_slope,
    'er_at_beta_127': er_127,
    'figure_path': figure_path,
}

# 打印结果供教师查阅
print("=" * 50)
print("CAPM SML 分析结果")
print("=" * 50)
print(f"无风险利率 (rf): {rf_init*100:.2f}%")
print(f"市场预期收益 (E[rm]): {erm_init*100:.2f}%")
print(f"SML 斜率 (市场风险溢价): {initial_slope*100:.2f}%")
print(f"Beta=1.27 处的期望收益: {er_127*100:.2f}%")
print(f"\n图形已保存至: {figure_path}")
print("=" * 50)

# 注意：plt.show() 不调用，因为要求保存文件。
# 若教师需要交互滑块，可取消下面注释并注释掉 savefig 后的退出：
# plt.show()

plt.close()  # 释放资源