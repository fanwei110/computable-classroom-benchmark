import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ==========================================
# 1. 参数设置 (将无风险利率与市场收益参数化)
# ==========================================
rf = 0.023      # 无风险利率: 2.3%
rm = 0.094      # 市场期望收益: 9.4%

# 股票数据: {名称: (beta, 实际期望收益)}
stocks = {
    'X': (0.62, 0.081),
    'Y': (1.18, 0.131),
    'Z': (1.51, 0.099)
}

# ==========================================
# 2. 核心计算 (SML斜率与指定Beta的期望收益)
# ==========================================
# SML斜率即为市场风险溢价
sml_slope = rm - rf

# 计算beta = 1.27处的CAPM期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 3. 绘图 (证券市场线与股票点标注)
# ==========================================
# 生成beta从0到2的连续数值用于画线
betas = np.linspace(0, 2, 100)
# SML期望收益: E(R) = rf + beta * (rm - rf)
ers_sml = rf + betas * sml_slope

plt.figure(figsize=(10, 7))

# 绘制SML
plt.plot(betas, ers_sml, label='Security Market Line (SML)', color='blue', linewidth=2.5)

# 绘制股票点并标注
for name, (beta, er) in stocks.items():
    # 计算Alpha：实际收益 - CAPM期望收益
    capm_er = rf + beta * sml_slope
    alpha = er - capm_er
    
    # 画散点
    plt.scatter(beta, er, color='red', zorder=5)
    
    # 标注内容：名称、Beta、收益、Alpha
    annotation_text = f'{name}\nβ={beta}, E(R)={er:.1%}\nα={alpha:.2%}'
    
    # 根据点的位置调整标注偏移，防止重叠
    if name == 'X':
        xytext_offset = (-15, 20)
    elif name == 'Y':
        xytext_offset = (15, 20)
    else: # Z
        xytext_offset = (-15, -40)
        
    plt.annotate(annotation_text, 
                 xy=(beta, er), 
                 xytext=xytext_offset,
                 textcoords='offset points',
                 bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.6),
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='black'))

# 绘制beta=1.27处的期望收益点
plt.scatter(beta_target, er_at_beta_127, color='green', marker='D', zorder=5)
plt.annotate(f'β={beta_target}, E(R)={er_at_beta_127:.2%}', 
             xy=(beta_target, er_at_beta_127), 
             xytext=(15, -25),
             textcoords='offset points',
             bbox=dict(boxstyle='round,pad=0.3', fc='lightgreen', alpha=0.6),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='black'))

# 格式化图表
plt.title('CAPM & Security Market Line (SML)', fontsize=16)
plt.xlabel('Beta (β)', fontsize=13)
plt.ylabel('Expected Return E(R)', fontsize=13)
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
plt.xlim(0, 2)
plt.ylim(0, 0.18)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=12)

# 将Y轴刻度格式化为百分比
plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=1))

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
fig_path = 'sml_plot.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# 输出结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': fig_path
}

# (可选) 打印验证，确保输出正确
print(f"SML Slope (Market Risk Premium): {result['sml_slope']:.4f} ({result['sml_slope']*100:.2f}%)")
print(f"Expected Return at beta=1.27: {result['er_at_beta_127']:.5f} ({result['er_at_beta_127']*100:.2f}%)")
print(f"Figure saved to: {result['figure_path']}")
