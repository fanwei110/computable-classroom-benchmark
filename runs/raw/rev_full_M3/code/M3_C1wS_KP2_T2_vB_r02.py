import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ==========================================
# 1. 参数化与核心计算
# ==========================================
# 初始参数假设：收益率以小数表示进行计算
rf_init = 2.3 / 100   # 无风险利率 2.3%
rm_init = 9.4 / 100   # 市场期望收益 9.4%

# SML斜率与特定Beta期望收益计算
sml_slope = rm_init - rf_init
er_at_beta_127 = rf_init + 1.27 * sml_slope

# 三只股票的数据 (Beta, 期望收益)
stocks = {
    'X': (0.62, 8.1 / 100),
    'Y': (1.18, 13.1 / 100),
    'Z': (1.51, 9.9 / 100)
}

# ==========================================
# 2. 绘制SML与证券点
# ==========================================
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25)  # 为底部滑块留出空间

beta_range = np.linspace(0, 2, 200)
sml_y_init = (rf_init + beta_range * (rm_init - rf_init)) * 100  # 转换为百分比显示

# 绘制SML线
sml_line, = ax.plot(beta_range, sml_y_init, 'b-', lw=2, label='SML')

# 标记无风险利率与市场组合点
rf_point = ax.scatter(0, rf_init * 100, color='black', s=80, zorder=5, label='Risk-Free Rate ($r_f$)')
rm_point = ax.scatter(1, rm_init * 100, color='orange', marker='*', s=200, zorder=5, label='Market Portfolio ($E(R_m)$)')

# 绘制股票点及Alpha偏离线 (偏离SML的部分即Alpha)
colors = ['red', 'green', 'purple']
alpha_lines = {}
for (name, (beta_val, er_val)), color in zip(stocks.items(), colors):
    sml_er_val = rf_init + beta_val * (rm_init - rf_init)
    
    # 股票散点
    ax.scatter(beta_val, er_val * 100, color=color, zorder=6, label=f'Stock {name}')
    ax.annotate(f'{name} ($\\beta$={beta_val})', 
                xy=(beta_val, er_val * 100), 
                xytext=(10, 5), textcoords='offset points', 
                fontsize=11, color=color, fontweight='bold')
    
    # Alpha偏离虚线 (从SML理论收益到实际收益)
    aline, = ax.plot([beta_val, beta_val], [sml_er_val * 100, er_val * 100], 
                     color=color, ls='--', lw=1.5, alpha=0.7)
    alpha_lines[name] = aline

# 动态信息文本：斜率与Beta=1.27的收益
info_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12,
                    verticalalignment='top', 
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

def update_info_text(current_rf, current_rm):
    current_slope = current_rm - current_rf
    current_er_127 = current_rf + 1.27 * current_slope
    info_text.set_text(f"SML Slope (Market Risk Premium): {current_slope*100:.2f}%\n"
                       f"E(R) at $\\beta$=1.27: {current_er_127*100:.2f}%")

update_info_text(rf_init, rm_init)

# 图表装饰
ax.set_xlabel('Beta ($\\beta$)', fontsize=12)
ax.set_ylabel('Expected Return (%)', fontsize=12)
ax.set_title('CAPM: Security Market Line (SML) & Alphas', fontsize=14)
ax.set_xlim(0, 2)
ax.set_ylim(0, 20)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='lower right', fontsize=10)

# ==========================================
# 3. 交互式滑块 (拖动修改rf与rm)
# ==========================================
ax_rf = plt.axes([0.15, 0.10, 0.70, 0.03])
ax_rm = plt.axes([0.15, 0.15, 0.70, 0.03])

slider_rf = Slider(ax_rf, '$r_f$ (%)', 0.0, 10.0, valinit=rf_init * 100, valstep=0.1)
slider_rm = Slider(ax_rm, '$E(R_m)$ (%)', 0.0, 20.0, valinit=rm_init * 100, valstep=0.1)

def update(val):
    rf_new = slider_rf.val / 100
    rm_new = slider_rm.val / 100
    
    # 更新SML线
    sml_line.set_ydata((rf_new + beta_range * (rm_new - rf_new)) * 100)
    
    # 更新rf与rm标记点
    rf_point.set_offsets([[0, rf_new * 100]])
    rm_point.set_offsets([[1, rm_new * 100]])
    
    # 更新各股票的Alpha偏离线
    for name, (beta_val, er_val) in stocks.items():
        sml_er_val = (rf_new + beta_val * (rm_new - rf_new)) * 100
        alpha_lines[name].set_ydata([sml_er_val, er_val * 100])
        
    # 更新信息文本
    update_info_text(rf_new, rm_new)
    
    fig.canvas.draw_idle()

slider_rf.on_changed(update)
slider_rm.on_changed(update)

# ==========================================
# 4. 保存图形与结果封装
# ==========================================
fig_path = 'sml_plot.png'
fig.savefig(fig_path, dpi=150, bbox_inches='tight')

# 填充结果字典
result = {
    'sml_slope': sml_slope,               # 0.071
    'er_at_beta_127': er_at_beta_127,     # 0.11317
    'figure_path': fig_path                # 'sml_plot.png'
}

# 若在交互式命令行运行可解除下行注释以查看交互窗口
# plt.show()
