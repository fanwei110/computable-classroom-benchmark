import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ==================== 可调参数的初始值 ====================
Rf_init = 0.023         # 无风险利率
ERm_init = 0.094        # 市场期望收益

# ==================== 股票数据 ====================
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# ==================== 计算初始斜率与特定点期望收益 ====================
slope = ERm_init - Rf_init               # SML 斜率
er_beta_127 = Rf_init + 1.27 * slope     # beta=1.27 处的期望收益

# ==================== 准备结果字典 ====================
result = {
    'sml_slope': slope,
    'er_at_beta_127': er_beta_127,
    'figure_path': 'sml.png'
}

# 输出到控制台，方便课堂上查看
print("=== CAPM & SML 结果 ===")
print(f"SML 斜率 (市场风险溢价): {slope:.4f} ({slope*100:.2f}%)")
print(f"Beta=1.27 处的 CAPM 期望收益: {er_beta_127:.4f} ({er_beta_127*100:.2f}%)")
print("结果已存入字典 `result`。")

# ==================== 绘图 ====================
plt.rcParams['font.size'] = 12
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.3)   # 为滑块留出空间

# 生成从 0 到 2 的 beta 序列
beta_vals = np.linspace(0, 2, 200)
line, = ax.plot(beta_vals, Rf_init + beta_vals * slope, 'b-', linewidth=2, label='Security Market Line')

# 无风险资产点
rf_point, = ax.plot(0, Rf_init, 'ko', markersize=8, label='Risk-Free Asset')
# 市场组合点
mkt_point, = ax.plot(1, ERm_init, 'ks', markersize=8, label='Market Portfolio')

# 股票 X, Y, Z
for name, (beta, ret) in stocks.items():
    ax.plot(beta, ret, 'ro', markersize=8)
    ax.annotate(f' {name}', (beta, ret), fontsize=11, fontweight='bold',
                textcoords="offset points", xytext=(8, 2), color='darkred')

# 装饰图形
ax.set_xlim(0, 2)
ax.set_xlabel('β (Beta)', fontsize=13)
ax.set_ylabel('Expected Return', fontsize=13)
ax.set_title('Security Market Line (SML) with Adjustable Parameters', fontsize=15)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='lower right')

# 显示当前斜率与 beta=1.27 期望收益的文本
text_info = ax.text(0.02, 0.95, 
                    f'Slope = {slope:.4f}\nE[R] at β=1.27 = {er_beta_127:.4f}',
                    transform=ax.transAxes, fontsize=11,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# ==================== 滑块（可调参数） ====================
axcolor = 'lightgoldenrodyellow'
ax_rf = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_erm = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)

s_rf = Slider(ax_rf, 'Risk-Free Rate', 0.0, 0.10, valinit=Rf_init, valfmt='%1.3f')
s_erm = Slider(ax_erm, 'Market Return', 0.05, 0.20, valinit=ERm_init, valfmt='%1.3f')

def update(val):
    """当滑块值改变时，更新 SML、特征点以及文本信息。"""
    rf = s_rf.val
    erm = s_erm.val
    new_slope = erm - rf
    new_er127 = rf + 1.27 * new_slope

    # 更新 SML 线
    line.set_ydata(rf + beta_vals * new_slope)
    # 更新无风险资产与市场组合点
    rf_point.set_ydata([rf])
    mkt_point.set_ydata([erm])
    # 更新信息文本
    text_info.set_text(f'Slope = {new_slope:.4f}\nE[R] at β=1.27 = {new_er127:.4f}')
    fig.canvas.draw_idle()

s_rf.on_changed(update)
s_erm.on_changed(update)

# ==================== 保存与显示 ====================
fig.savefig(result['figure_path'], dpi=150, bbox_inches='tight')
plt.show()
