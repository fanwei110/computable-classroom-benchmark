import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ================== 可调参数（初始值） ==================
R_f_init = 0.023      # 无风险利率 2.3%
E_R_m_init = 0.094    # 市场期望收益 9.4%

# ================== 股票数据 ==========================
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# ================== 绘图初始化 =========================
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)          # 为滑块留出空间

beta_range = np.linspace(0, 2, 200)       # beta 从 0 到 2
sml_line, = ax.plot(beta_range,
                    R_f_init + beta_range * (E_R_m_init - R_f_init),
                    'b-', linewidth=2, label='Security Market Line')

# 无风险资产点
rf_point, = ax.plot(0, R_f_init, 'go', markersize=8, label='Risk-free rate')

# 股票 X, Y, Z
for name, s in stocks.items():
    ax.plot(s['beta'], s['return'], 'ro', markersize=7)
    ax.annotate(f' {name}',
                (s['beta'], s['return']),
                textcoords="offset points",
                xytext=(8, 5),
                fontsize=10,
                fontweight='bold')

# 格式
ax.set_xlabel('Beta', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.35)
ax.legend(loc='upper left')

# ================== 滑块 ==============================
ax_rf = plt.axes([0.20, 0.12, 0.65, 0.03])
ax_mr = plt.axes([0.20, 0.06, 0.65, 0.03])

slider_rf = Slider(ax_rf, 'Risk-free rate', 0.0, 0.05,
                   valinit=R_f_init, valfmt='%1.3f')
slider_mr = Slider(ax_mr, 'Market return', 0.05, 0.20,
                   valinit=E_R_m_init, valfmt='%1.3f')

def update(val):
    R_f = slider_rf.val
    E_R_m = slider_mr.val
    sml_line.set_ydata(R_f + beta_range * (E_R_m - R_f))
    rf_point.set_ydata([R_f])
    fig.canvas.draw_idle()

slider_rf.on_changed(update)
slider_mr.on_changed(update)

# ================== 保存静态图 =========================
figure_path = 'sml_plot.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')

# ================== 计算要求指标 =======================
# SML 斜率 = 市场风险溢价
sml_slope = E_R_m_init - R_f_init          # 0.071

# beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = R_f_init + beta_target * sml_slope   # 0.11317

# ================== 输出契约 ==========================
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

print(result)

# ================== 显示交互窗口 =======================
plt.show()
