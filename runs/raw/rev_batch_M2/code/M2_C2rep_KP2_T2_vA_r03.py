import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import os

# ========================
# 1. 初始参数与数据
# ========================
# 无风险利率 (年化)
rf_init = 0.023   # 2.3%
# 市场期望收益 (年化)
rm_init = 0.094   # 9.4%

# 股票数据：beta, 实际收益, 标签
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 用于计算 SML 的 beta 范围
beta_range = np.linspace(0, 2, 200)

# ========================
# 2. 创建图形与静态元素
# ========================
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25)  # 为滑块留空间

# 初始 SML 线
market_risk_premium_init = rm_init - rf_init
sml_init = rf_init + beta_range * market_risk_premium_init
line, = ax.plot(beta_range, sml_init, 'b-', lw=2, label='SML (Security Market Line)')

# 无风险资产点 (beta=0)
ax.plot(0, rf_init, 'ko', markersize=8, label=f'Rf = {rf_init*100:.1f}%')
# 市场组合点 (beta=1)
ax.plot(1, rm_init, 'ko', markersize=8, label=f'Market = {rm_init*100:.1f}%')

# 画出三只股票
colors = ['red', 'green', 'orange']
for (label, data), color in zip(stocks.items(), colors):
    b = data['beta']
    r = data['return']
    ax.scatter(b, r, c=color, s=100, zorder=5, edgecolors='black')
    ax.annotate(f'  Stock {label}\n  β={b:.2f}, r={r*100:.2f}%',
                (b, r), textcoords="offset points", xytext=(10, -15),
                fontsize=9, color=color, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=color, lw=1.2))

# 图例与标签
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return', fontsize=12)
ax.set_title(f'Security Market Line: E(R) = {rf_init*100:.2f}% + β * {market_risk_premium_init*100:.2f}%',
             fontsize=14)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left')
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.20)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.1f}%'.format(y*100)))

# ========================
# 3. 参数化滑块
# ========================
axcolor = 'lightgoldenrodyellow'
ax_rf = plt.axes([0.15, 0.10, 0.70, 0.03], facecolor=axcolor)
ax_rm = plt.axes([0.15, 0.05, 0.70, 0.03], facecolor=axcolor)

slider_rf = Slider(ax_rf, 'Risk-Free Rate', 0.0, 0.10, valinit=rf_init, valfmt='%1.3f')
slider_rm = Slider(ax_rm, 'Market Return', 0.05, 0.20, valinit=rm_init, valfmt='%1.3f')

# SML 上方显示 beta=1.27 信息
info_text = ax.text(0.5, 0.95, '', transform=ax.transAxes, fontsize=11,
                    verticalalignment='top', horizontalalignment='center',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

def update(val):
    rf = slider_rf.val
    rm = slider_rm.val
    mrp = rm - rf
    new_sml = rf + beta_range * mrp
    line.set_ydata(new_sml)

    # 更新标题
    ax.set_title(f'Security Market Line: E(R) = {rf*100:.2f}% + β * {mrp*100:.2f}%', fontsize=14)

    # 计算 beta=1.27 处的期望收益
    er_127 = rf + 1.27 * mrp
    info_text.set_text(f'Slope (Market Risk Premium) = {mrp*100:.2f}%\n'
                       f'E(R) at β=1.27 = {er_127*100:.2f}%')

    fig.canvas.draw_idle()

# 绑定滑块更新
slider_rf.on_changed(update)
slider_rm.on_changed(update)

# 初始触发一次以显示信息
update(None)

# ========================
# 4. 保存图形并构建结果字典
# ========================
figure_path = os.path.abspath('sml_capm.png')
fig.savefig(figure_path, dpi=150, bbox_inches='tight')

# 最终结果（基于初始参数的报告）
final_slope = market_risk_premium_init            # rm - rf
final_er_at_127 = rf_init + 1.27 * final_slope    # CAPM 期望收益

result = {
    'sml_slope': final_slope,
    'er_at_beta_127': final_er_at_127,
    'figure_path': figure_path
}

# 打印结果供课堂查看
print("=== CAPM SML 分析结果 ===")
print(f"证券市场线斜率 (市场风险溢价) : {final_slope*100:.2f}%")
print(f"β = 1.27 处的 CAPM 期望收益 : {final_er_at_127*100:.2f}%")
print(f"图形已保存至 : {figure_path}")
print("\n字典 result =", result)

# 显示交互界面（若在支持的环境中运行）
plt.show()
