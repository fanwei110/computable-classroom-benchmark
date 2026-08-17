import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ==========================================
# 1. 参数定义与核心计算
# ==========================================
# 初始参数（以百分比形式表示以符合直觉，计算时注意转换）
rf_init = 2.3   # 无风险利率 %
rm_init = 9.4   # 市场期望收益 %

# 股票数据：X(0.62, 8.1%), Y(1.18, 13.1%), Z(1.51, 9.9%)
stocks = {
    'X': {'beta': 0.62, 'er': 8.1},
    'Y': {'beta': 1.18, 'er': 13.1},
    'Z': {'beta': 1.51, 'er': 9.9}
}

# 根据初始参数计算要求的指标
sml_slope_pct = rm_init - rf_init                 # 斜率，百分比表示 7.1%
sml_slope_dec = sml_slope_pct / 100.0             # 斜率，小数表示 0.071

beta_target = 1.27
er_at_beta_127_pct = rf_init + beta_target * (rm_init - rf_init)  # 11.317%
er_at_beta_127_dec = er_at_beta_127_pct / 100.0                   # 0.11317

# ==========================================
# 2. 绘图与交互设置
# ==========================================
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.25)  # 为底部滑块留出空间

# 绘制SML和股票点的函数
def plot_sml(rf, rm):
    ax.clear()
    
    # SML线的Beta范围
    beta_range = np.linspace(0, 2, 100)
    # SML公式: E(R) = rf + beta * (rm - rf)
    er_sml = rf + beta_range * (rm - rf)
    
    # 绘制SML
    ax.plot(beta_range, er_sml, label='SML (证券市场线)', color='royalblue', linewidth=2.5, zorder=2)
    
    # 绘制股票点及Alpha偏离线
    colors = {'X': 'crimson', 'Y': 'forestgreen', 'Z': 'darkorchid'}
    for name, data in stocks.items():
        beta_i = data['beta']
        er_i = data['er']
        
        # 计算该Beta对应的SML理论收益
        er_sml_i = rf + beta_i * (rm - rf)
        
        # 绘制偏离线 (Alpha)
        ax.plot([beta_i, beta_i], [er_sml_i, er_i], color=colors[name], linestyle='--', linewidth=1.5, zorder=3)
        # 绘制实际收益点
        ax.scatter(beta_i, er_i, color=colors[name], zorder=5, s=80, label=f'股票 {name} (β={beta_i}, E(R)={er_i}%)')
        
        # 标注Alpha值
        alpha_val = er_i - er_sml_i
        offset_y = 10 if alpha_val >= 0 else -15
        ax.annotate(f'α={alpha_val:.2f}%', (beta_i, er_i), textcoords="offset points", 
                    xytext=(10, offset_y), ha='center', fontsize=9, color=colors[name], fontweight='bold')

    # 标注 rf 和 rm 点
    ax.scatter(0, rf, color='black', zorder=5, s=60)
    ax.scatter(1, rm, color='black', zorder=5, s=60)
    ax.annotate(f'Rf={rf:.1f}%', (0, rf), textcoords="offset points", xytext=(10, -10), fontsize=10)
    ax.annotate(f'Market={rm:.1f}%', (1, rm), textcoords="offset points", xytext=(10, -10), fontsize=10)

    # 坐标轴与格式
    ax.set_xlabel('Beta (β)', fontsize=12)
    ax.set_ylabel('Expected Return E(R) (%)', fontsize=12)
    ax.set_title('CAPM 与 证券市场线 (SML) - 拖动滑块调整参数', fontsize=14)
    ax.set_xlim(0, 2)
    
    # 动态调整Y轴范围以适应滑块变化
    y_min = min(0, rf - 2)
    y_max = max(20, rm + 2 * (rm - rf) + 2)
    ax.set_ylim(y_min, y_max)
    
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend(loc='upper left', fontsize=9)

    # 动态信息框（随滑块更新）
    current_slope = rm - rf
    current_er_127 = rf + 1.27 * (rm - rf)
    info_text = f'当前 SML 斜率: {current_slope:.2f}%\nβ=1.27 对应的 E(R): {current_er_127:.2f}%'
    ax.text(0.98, 0.05, info_text, transform=ax.transAxes, fontsize=11,
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# 初始绘制
plot_sml(rf_init, rm_init)

# 添加交互滑块
ax_rf = plt.axes([0.15, 0.10, 0.65, 0.03])
ax_rm = plt.axes([0.15, 0.05, 0.65, 0.03])

slider_rf = Slider(ax_rf, '无风险利率 Rf(%)', 0.0, 10.0, valinit=rf_init, valstep=0.1)
slider_rm = Slider(ax_rm, '市场收益 Rm(%)', 0.0, 20.0, valinit=rm_init, valstep=0.1)

# 滑块更新回调
def update(val):
    plot_sml(slider_rf.val, slider_rm.val)

slider_rf.on_changed(update)
slider_rm.on_changed(update)

# ==========================================
# 3. 保存图形与封装输出
# ==========================================
figure_path = 'sml_capm_plot.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')

# 按照输出契约构建 result 字典 (采用小数形式以符合金融计算标准)
result = {
    'sml_slope': sml_slope_dec,          # 0.071
    'er_at_beta_127': er_at_beta_127_dec,# 0.11317
    'figure_path': figure_path
}

# 控制台输出报告，方便课堂展示
print("="*50)
print("《证券投资学》课堂演示 - CAPM与SML计算结果")
print("="*50)
print(f"初始参数: Rf = {rf_init}%, Rm = {rm_init}%")
print(f"SML斜率 (市场风险溢价) : {sml_slope_pct:.1f}% (即 {sml_slope_dec})")
print(f"Beta = 1.27 对应的期望收益: {er_at_beta_127_pct:.3f}% (即 {er_at_beta_127_dec})")
print(f"图形已保存至: {figure_path}")
print("="*50)
print("提示: 运行脚本后可拖动图表下方的滑块动态调整 Rf 和 Rm 观察变化。")

# plt.show()  # 课堂投屏时取消注释此行以展示动态交互
