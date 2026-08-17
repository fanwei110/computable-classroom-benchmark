import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

# ── 初始参数 ──
rf_init = 0.023          # 无风险利率 2.3%
rm_init = 0.094          # 市场收益率 9.4%

# ── 三个资产点 ──
points = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# ── SML 公式 ──
def sml_er(beta, rf, rm):
    return rf + beta * (rm - rf)

def sml_slope(rf, rm):
    return rm - rf

# ── 初始计算 ──
slope_init = sml_slope(rf_init, rm_init)          # 0.071
er_127_init = sml_er(1.27, rf_init, rm_init)      # 0.11317

# ── 绘图 ──
fig, ax = plt.subplots(figsize=(11, 7))
plt.subplots_adjust(bottom=0.25)

beta_range = np.linspace(0, 2, 200)

# SML 线
sml_line, = ax.plot(beta_range,
                    sml_er(beta_range, rf_init, rm_init),
                    'b-', linewidth=2, label='SML')

# 三个资产点
for name, (b, r) in points.items():
    ax.plot(b, r, 'ro', markersize=8, zorder=5)
    ax.annotate(f'{name}({b}, {r*100:.1f}%)',
                xy=(b, r), xytext=(12, 8),
                textcoords='offset points', fontsize=9,
                arrowprops=dict(arrowstyle='->', lw=0.8))

# rf 点 & 市场点
rf_pt, = ax.plot(0, rf_init, 'g^', markersize=10, zorder=5, label='Rf')
mkt_pt, = ax.plot(1, rm_init, 'gs', markersize=10, zorder=5, label='Market')

# beta=1.27 对应收益的标注
er127_pt, = ax.plot(1.27, er_127_init, 'cD', markersize=9, zorder=5,
                    label=f'β=1.27 → {er_127_init*100:.2f}%')
er127_label = ax.annotate(f'β=1.27: {er_127_init*100:.2f}%',
                          xy=(1.27, er_127_init), xytext=(14, -18),
                          textcoords='offset points', fontsize=9, color='darkcyan',
                          arrowprops=dict(arrowstyle='->', color='darkcyan', lw=0.8))

# 斜率文本
slope_text = ax.text(0.02, 0.96,
                     f'Slope = Rm − Rf = {slope_init*100:.1f}%',
                     transform=ax.transAxes, fontsize=11,
                     verticalalignment='top',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

# 坐标轴
ax.set_xlabel('Beta', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Security Market Line (SML) — 拖动滑块调整 Rf / Rm',
             fontsize=13)
ax.set_xlim(-0.05, 2.15)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y*100:.1f}%'))
ax.legend(loc='lower right', fontsize=9)
ax.grid(True, alpha=0.3)

# ── 滑块 ──
ax_rf = plt.axes([0.2, 0.10, 0.6, 0.03])
ax_rm = plt.axes([0.2, 0.04, 0.6, 0.03])

sl_rf = Slider(ax_rf, 'Rf', 0.0, 0.10, valinit=rf_init, valstep=0.001,
               valfmt='%.1f%%')
sl_rm = Slider(ax_rm, 'Rm', 0.01, 0.20, valinit=rm_init, valstep=0.001,
               valfmt='%.1f%%')

def update(val):
    rf = sl_rf.val
    rm = sl_rm.val
    slp = sml_slope(rf, rm)
    er127 = sml_er(1.27, rf, rm)

    # SML 线
    sml_line.set_ydata(sml_er(beta_range, rf, rm))
    # rf / market 点
    rf_pt.set_ydata([rf])
    mkt_pt.set_ydata([rm])
    # beta=1.27 点
    er127_pt.set_ydata([er127])
    er127_label.set_position((er127_label.xy[0] + 14, er127_label.xy[1] - 18))
    er127_label.xy = (1.27, er127)
    er127_label.set_text(f'β=1.27: {er127*100:.2f}%')
    # 斜率文本
    slope_text.set_text(f'Slope = Rm − Rf = {slp*100:.1f}%')

    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

sl_rf.on_changed(update)
sl_rm.on_changed(update)

# ── 保存 ──
fig_path = '/tmp/sml_plot.png'
fig.savefig(fig_path, dpi=150, bbox_inches='tight')

# ── 结果字典 ──
result = {
    'sml_slope': sml_slope(rf_init, rm_init),        # 0.071
    'er_at_beta_127': sml_er(1.27, rf_init, rm_init),# 0.11317
    'figure_path': fig_path
}

print("=== 结果 ===")
print(f"SML 斜率 (Rm - Rf): {result['sml_slope']:.4f}  ({result['sml_slope']*100:.1f}%)")
print(f"Beta=1.27 期望收益:  {result['er_at_beta_127']:.5f} ({result['er_at_beta_127']*100:.2f}%)")
print(f"图片路径: {result['figure_path']}")
print(result)
