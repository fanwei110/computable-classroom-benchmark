import matplotlib.pyplot as plt
import numpy as np

# 初始参数
rf = 0.023
market_ret = 0.094
sml_slope = market_ret - rf  # 直接基于给定参数的斜率

# 给定的点
X = (0.62, 0.081)
Y = (1.18, 0.131)
Z = (1.51, 0.099)

# Beta 1.27 对应收益
beta_127 = 1.27
er_at_beta_127 = rf + sml_slope * beta_127

# 绘制 SML
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.25)

# SML 线（初始：rf=2.3%, 市场=9.4%）
beta_vals = np.linspace(0, 2, 100)
sml_line, = ax.plot(beta_vals, rf + sml_slope * beta_vals, 'k-', label='SML')

# 标注 rf 和 市场点（可拖动）
rf_point, = ax.plot(0, rf, 'bo', markersize=8, label='rf')
market_point, = ax.plot(1, market_ret, 'go', markersize=8, label='Market')

# 标注 X, Y, Z
ax.plot(*X, 'rx', markersize=8, label='X')
ax.plot(*Y, 'mx', markersize=8, label='Y')
ax.plot(*Z, 'cx', markersize=8, label='Z')

# 坐标轴设置
ax.set_xlabel('Beta')
ax.set_ylabel('Expected Return')
ax.set_title('Security Market Line (SML)')
ax.grid(True)
ax.legend()
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.2)

# 当前参数显示文字
param_text = ax.text(0.5, -0.25, f'rf={rf:.2%}  Market={market_ret:.2%}  Slope={sml_slope:.3f}',
                     transform=ax.transAxes, ha='center', fontsize=10)

# ---- 交互拖动功能 ----
dragging = None

def on_press(event):
    global dragging
    if event.inaxes != ax:
        return
    contains_rf, _ = rf_point.contains(event)
    contains_mkt, _ = market_point.contains(event)
    if contains_rf:
        dragging = 'rf'
    elif contains_mkt:
        dragging = 'market'

def on_motion(event):
    global rf, market_ret, sml_slope, er_at_beta_127
    if dragging is None or event.inaxes != ax:
        return
    y = event.ydata
    if dragging == 'rf':
        rf = max(0, y)  # 限制非负
        rf_point.set_ydata([rf])
    elif dragging == 'market':
        market_ret = max(0, y)
        market_point.set_ydata([market_ret])

    # 更新 SML 斜率和线
    sml_slope = market_ret - rf
    sml_line.set_ydata(rf + sml_slope * beta_vals)

    # 更新 Beta 1.27 对应的收益
    er_at_beta_127 = rf + sml_slope * beta_127

    # 更新参数文字提示
    param_text.set_text(f'rf={rf:.2%}  Market={market_ret:.2%}  Slope={sml_slope:.3f}')
    fig.canvas.draw_idle()

def on_release(event):
    global dragging
    dragging = None

fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('motion_notify_event', on_motion)
fig.canvas.mpl_connect('button_release_event', on_release)

# 保存图像
figure_path = 'sml_chart.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.show()

# 结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

print("SML斜率:", result['sml_slope'])
print("Beta 1.27对应收益:", result['er_at_beta_127'])
print("图保存路径:", result['figure_path'])
