import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# =========================
# 参数初始化
# =========================
Rf_init = 0.023     # 无风险利率
Rm_init = 0.094     # 市场期望收益

# =========================
# 工具函数：SML 公式
# =========================
def sml_line(beta, rf, rm):
    """根据 beta 数组返回 SML 上的期望收益"""
    return rf + beta * (rm - rf)

# =========================
# 准备数据
# =========================
beta_range = np.linspace(0, 2, 200)  # Beta 0 到 2

# 三只股票：{名称: (beta, 实际收益)}
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# =========================
# 创建图形与交互滑块
# =========================
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)  # 给滑块留空间

# 绘制初始 SML
sml_curve, = ax.plot(beta_range,
                     sml_line(beta_range, Rf_init, Rm_init),
                     'b-', linewidth=2, label='SML')

# 标出市场组合 (beta=1) 与无风险资产 (beta=0)
market_pt, = ax.plot(1.0,
                     sml_line(1.0, Rf_init, Rm_init),
                     'ko', markersize=8, label='Market Portfolio')
rf_pt, = ax.plot(0.0,
                 Rf_init,
                 'ks', markersize=8, label='Risk-Free Asset')

# 标出三只股票
for name, (b, r) in stocks.items():
    ax.plot(b, r, 'ro', markersize=8)
    ax.annotate(name, (b, r),
                textcoords="offset points",
                xytext=(6, 6),
                fontsize=12, fontweight='bold', color='darkred')

# 图表装饰
ax.set_xlabel('Beta (β)', fontsize=13)
ax.set_ylabel('Expected Return', fontsize=13)
ax.set_title('Security Market Line (SML) — CAPM', fontsize=15)
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.22)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='lower right', fontsize=10)

# 创建参数滑块
ax_rf = plt.axes([0.2, 0.12, 0.6, 0.03])   # 无风险利率滑块
ax_rm = plt.axes([0.2, 0.06, 0.6, 0.03])   # 市场收益滑块

slider_rf = Slider(ax_rf, 'Risk-Free Rate', 0.0, 0.1,
                   valinit=Rf_init, valstep=0.0005)
slider_rm = Slider(ax_rm, 'Market Return', 0.01, 0.2,
                   valinit=Rm_init, valstep=0.0005)

# =========================
# 滑块回调：实时更新 SML
# =========================
def update(val):
    rf = slider_rf.val
    rm = slider_rm.val
    # 更新 SML 曲线
    sml_curve.set_ydata(sml_line(beta_range, rf, rm))
    # 更新市场组合与无风险资产的位置
    market_pt.set_ydata(sml_line(1.0, rf, rm))
    rf_pt.set_ydata(rf)
    # 股票点保持不变（它们的实际收益固定）
    fig.canvas.draw_idle()

slider_rf.on_changed(update)
slider_rm.on_changed(update)

# =========================
# 保存初始静态图像
# =========================
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')

# =========================
# 计算要求的结果
# =========================
sml_slope = Rm_init - Rf_init                     # SML 斜率（市场风险溢价）
er_at_beta_127 = Rf_init + 1.27 * sml_slope       # β=1.27 的 CAPM 期望收益

result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

print("========== 输出结果 ==========")
print(f"SML 斜率（市场风险溢价）：{sml_slope:.4f} ({sml_slope*100:.2f}%)")
print(f"β = 1.27 处的 CAPM 期望收益：{er_at_beta_127:.4f} ({er_at_beta_127*100:.2f}%)")
print(f"图形已保存至：{figure_path}")
print("结果字典：", result)

# 显示交互图（在脚本环境中会弹出窗口，在 Notebook 中需 %matplotlib notebook）
plt.show()
