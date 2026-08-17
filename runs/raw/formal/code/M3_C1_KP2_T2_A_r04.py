import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

# ==================== 参数设置 ====================
rf_init = 2.3    # 无风险利率 (%)
rm_init = 9.4    # 市场期望收益 (%)

# ==================== 计算 ====================
sml_slope = rm_init - rf_init                          # SML斜率 (%)
er_at_beta_127 = rf_init + 1.27 * (rm_init - rf_init) # beta=1.27的期望收益 (%)

# ==================== 绘图 ====================
fig, ax = plt.subplots(figsize=(11, 7))
plt.subplots_adjust(bottom=0.28)

beta_range = np.linspace(0, 2, 300)

def sml(beta, rf_val, rm_val):
    return rf_val + beta * (rm_val - rf_val)

# --- SML 线 ---
line, = ax.plot(beta_range, sml(beta_range, rf_init, rm_init),
                'b-', linewidth=2.5, label='SML', zorder=2)

# --- 三个资产点 ---
points = {'X': (0.62, 8.1), 'Y': (1.18, 13.1), 'Z': (1.51, 9.9)}
offsets = {'X': (8, 12), 'Y': (8, 8), 'Z': (8, -18)}  # 标注偏移防重叠
for name, (b, er) in points.items():
    ax.scatter(b, er, s=120, zorder=5, edgecolors='black', linewidths=0.8)
    ax.annotate(f'{name} (β={b}, E(R)={er}%)',
                (b, er), textcoords="offset points",
                xytext=offsets[name], fontsize=10,
                arrowprops=dict(arrowstyle='->', color='gray', lw=0.8))

# --- 市场组合 & 无风险利率 ---
mkt_dot = ax.scatter(1, rm_init, color='blue', s=130, marker='D',
                     zorder=5, edgecolors='black', linewidths=0.8, label='Market')
mkt_annot = ax.annotate(f'M (1, {rm_init}%)', (1, rm_init),
                         textcoords="offset points", xytext=(12, -18), fontsize=10)

rf_dot = ax.scatter(0, rf_init, color='green', s=130, marker='o',
                    zorder=5, edgecolors='black', linewidths=0.8, label='Rf')
rf_annot = ax.annotate(f'Rf (0, {rf_init}%)', (0, rf_init),
                        textcoords="offset points", xytext=(12, -18), fontsize=10)

# --- 样式 ---
ax.set_xlabel('Beta (β)', fontsize=13)
ax.set_ylabel('Expected Return E(R) (%)', fontsize=13)
ax.set_title('Security Market Line (SML)', fontsize=15, fontweight='bold')
ax.set_xlim(-0.05, 2.15)
ax.set_ylim(-1, 20)
ax.axhline(y=0, color='grey', linewidth=0.5)
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left', fontsize=11)

# --- 斜率/信息文本框 ---
info_text = ax.text(1.55, 3.0, '', fontsize=10,
                    bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.9))

def update_info(rf_val, rm_val):
    slope = rm_val - rf_val
    er127 = rf_val + 1.27 * slope
    info_text.set_text(
        f'SML斜率 = {slope:.2f}%\n'
        f'E(R)|β=1.27 = {er127:.2f}%'
    )

update_info(rf_init, rm_init)

# ==================== 滑块 ====================
ax_rf = plt.axes([0.2, 0.12, 0.6, 0.03])
ax_rm = plt.axes([0.2, 0.06, 0.6, 0.03])

slider_rf = Slider(ax_rf, 'Rf (%)', 0.0, 10.0, valinit=rf_init, valstep=0.1, color='lightgreen')
slider_rm = Slider(ax_rm, 'E(Rm) (%)', 1.0, 20.0, valinit=rm_init, valstep=0.1, color='lightskyblue')

def on_slider_change(val):
    rf_new = slider_rf.val
    rm_new = slider_rm.val
    # 更新SML线
    line.set_ydata(sml(beta_range, rf_new, rm_new))
    # 更新市场组合点
    mkt_dot.set_offsets([[1, rm_new]])
    mkt_annot.set_text(f'M (1, {rm_new:.1f}%)')
    mkt_annot.xy = (1, rm_new)
    # 更新无风险利率点
    rf_dot.set_offsets([[0, rf_new]])
    rf_annot.set_text(f'Rf (0, {rf_new:.1f}%)')
    rf_annot.xy = (0, rf_new)
    # 更新信息框
    update_info(rf_new, rm_new)
    fig.canvas.draw_idle()

slider_rf.on_changed(on_slider_change)
slider_rm.on_changed(on_slider_change)

# ==================== 保存 ====================
figure_path = '/mnt/data/sml_plot.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 输出结果 ====================
result = {
    'sml_slope': round(sml_slope, 2),            # 7.1 (%)
    'er_at_beta_127': round(er_at_beta_127, 3),  # 11.317 (%)
    'figure_path': figure_path
}

print(result)
