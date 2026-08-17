import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 初始参数（百分比形式，便于滑块显示，内部计算用小数）
rf_init = 2.3       # 无风险利率 %
rm_init = 9.4       # 市场收益率 %
beta_range = np.linspace(0, 2, 100)

# 三只股票的数据
stocks = {
    'X': (0.62, 8.1),
    'Y': (1.18, 13.1),
    'Z': (1.51, 9.9)
}

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)  # 为滑块留空间

# 初始 SML 线
sml_line, = ax.plot(beta_range, rf_init + beta_range * (rm_init - rf_init),
                    'b-', lw=2, label='SML')
# 市场组合点（beta=1）
market_point, = ax.plot(1, rm_init, 'ko', markersize=8, label='Market')
# 无风险资产点（beta=0）
rf_point, = ax.plot(0, rf_init, 'ko', markersize=8)

# 绘制三只股票
colors = ['red', 'green', 'orange']
for (name, (beta, er)), color in zip(stocks.items(), colors):
    ax.plot(beta, er, 'o', color=color, markersize=8)
    ax.annotate(name, (beta, er), textcoords="offset points", xytext=(5,5),
                fontsize=12, color=color)

# 装饰
ax.set_xlabel('Beta', fontsize=12)
ax.set_ylabel('Expected Return (%)', fontsize=12)
ax.set_title('Security Market Line (SML)', fontsize=14)
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_xlim(0, 2)
ax.set_ylim(0, 20)  # 留出足够空间
ax.legend()

# 添加动态文本显示斜率和特定 beta 的期望收益
text_slope = ax.text(1.5, 2, '', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))
text_er = ax.text(1.5, 1, '', fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

# 创建滑块轴
ax_rf = plt.axes([0.2, 0.1, 0.65, 0.03])
ax_rm = plt.axes([0.2, 0.05, 0.65, 0.03])

slider_rf = Slider(ax_rf, 'Risk-Free Rate (%)', 0.0, 10.0, valinit=rf_init, valstep=0.1)
slider_rm = Slider(ax_rm, 'Market Return (%)', 5.0, 20.0, valinit=rm_init, valstep=0.1)

# 更新函数
def update(val):
    rf = slider_rf.val
    rm = slider_rm.val
    # 更新 SML 线
    sml_line.set_ydata(rf + beta_range * (rm - rf))
    # 更新市场点和无风险点
    market_point.set_ydata([rm])
    rf_point.set_ydata([rf])
    # 计算斜率（市场风险溢价，百分比）
    slope = rm - rf
    # beta=1.27 的期望收益
    beta_target = 1.27
    er_target = rf + beta_target * slope
    # 更新文本
    text_slope.set_text(f'Slope (Market Risk Premium): {slope:.2f}%')
    text_er.set_text(f'Expected Return at beta={beta_target}: {er_target:.2f}%')
    fig.canvas.draw_idle()

# 连接滑块
slider_rf.on_changed(update)
slider_rm.on_changed(update)

# 初始化文本
update(None)

# 显示交互窗口
plt.show()

# 交互结束后，获取最终滑块值，计算最终结果（小数形式）
rf_final = slider_rf.val / 100.0
rm_final = slider_rm.val / 100.0
slope_final = rm_final - rf_final
er_at_beta_127 = rf_final + 1.27 * slope_final

# 保存图形（当前状态）
figure_path = 'sml.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')

# 结果字典
result = {
    'sml_slope': round(slope_final, 6),
    'er_at_beta_127': round(er_at_beta_127, 6),
    'figure_path': figure_path
}

print("结果：")
print(result)
