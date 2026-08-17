import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数化设置 (Parameterized Variables)
# ==========================================
Rf = 0.023  # 无风险利率 2.3%
Rm = 0.094  # 市场期望收益 9.4%

# ==========================================
# 2. 核心计算 (Calculations)
# ==========================================
# SML斜率即为市场风险溢价
sml_slope = Rm - Rf

# beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = Rf + beta_target * sml_slope

# ==========================================
# 3. 绘制证券市场线与股票点 (Plotting SML & Stocks)
# ==========================================
# 生成 beta 从 0 到 2 的序列
betas = np.linspace(0, 2, 100)
# SML 对应的期望收益
sml_returns = Rf + betas * sml_slope

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099},
}

plt.figure(figsize=(10, 7))

# 绘制 SML 直线 (转为百分比显示以符合金融习惯)
plt.plot(betas, sml_returns * 100, label='Security Market Line (SML)', 
         color='blue', linewidth=2.5, zorder=2)

# 标出无风险利率与市场收益点
plt.scatter(0, Rf * 100, color='green', s=80, zorder=3, label=f'Risk-Free Rate ({Rf*100:.1f}%)')
plt.scatter(1, Rm * 100, color='purple', s=80, zorder=3, label=f'Market Return ({Rm*100:.1f}%)')

# 绘制并标注股票 X, Y, Z
markers = {'X': 'o', 'Y': 's', 'Z': '^'}
for name, data in stocks.items():
    b = data['beta']
    r = data['return']
    # 计算 Alpha (偏离 SML 的部分)
    alpha = r - (Rf + b * sml_slope)
    
    plt.scatter(b, r * 100, marker=markers[name], s=120, zorder=4, edgecolor='black')
    # 标注文字 (包含 Beta, 收益率与 Alpha)
    annotation_text = f"{name}\nβ={b:.2f}, r={r*100:.1f}%\nα={alpha*100:.2f}%"
    plt.annotate(annotation_text, 
                 xy=(b, r * 100), 
                 xytext=(15, 10), 
                 textcoords='offset points',
                 fontsize=10,
                 bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.7),
                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2'))

# 格式化图表
plt.title('CAPM & Security Market Line', fontsize=16, fontweight='bold')
plt.xlabel('Beta (β)', fontsize=13)
plt.ylabel('Expected Return (%)', fontsize=13)
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.xlim(0, 2)
plt.ylim(0, 16)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11, loc='upper left')

# 添加公式水印
plt.text(1.5, 1.5, r'$E(R_i) = R_f + \beta_i (E(R_m) - R_f)$', 
         fontsize=14, color='gray', alpha=0.6,
         ha='center', va='center')

# ==========================================
# 4. 保存图形与结果输出 (Save & Output)
# ==========================================
fig_path = 'sml_capm_plot.png'
plt.savefig(fig_path, dpi=200, bbox_inches='tight')
plt.close()

# 填充结果字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': fig_path
}

# 用于课堂验证的打印输出 (可按需注释)
if __name__ == '__main__':
    print("--- 计算结果报告 ---")
    print(f"SML 斜率 (市场风险溢价): {result['sml_slope']:.4f} ({result['sml_slope']*100:.2f}%)")
    print(f"Beta=1.27 处的 CAPM 期望收益: {result['er_at_beta_127']:.5f} ({result['er_at_beta_127']*100:.2f}%)")
    print(f"图形已保存至: {result['figure_path']}")
