import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 参数化无风险利率与市场期望收益
# ==========================================
rf = 0.023   # 无风险利率 2.3%
rm = 0.094   # 市场期望收益 9.4%

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# ==========================================
# 2. 计算 SML 斜率与 beta=1.27 处的期望收益
# ==========================================
sml_slope = rm - rf
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 3. 绘制证券市场线 (SML) 与股票标注点
# ==========================================
# 生成 beta 序列与 SML 对应的期望收益
betas_line = np.linspace(0, 2, 100)
er_line = rf + betas_line * sml_slope

# 创建画布
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制 SML
ax.plot(betas_line, er_line, color='blue', linewidth=2.5, label='SML: $E(R) = R_f + \\beta (E(R_M) - R_f)$')

# 标出无风险利率与市场组合点
ax.scatter(0, rf, color='green', s=80, zorder=5, label=f'Risk-Free Rate ({rf:.1%})')
ax.scatter(1, rm, color='orange', s=80, zorder=5, label=f'Market Portfolio ({rm:.1%})')

# 绘制股票点并标注 (Alpha 为偏离 SML 的部分)
colors = {'X': 'red', 'Y': 'purple', 'Z': 'brown'}
for name, data in stocks.items():
    beta_i = data['beta']
    ret_i = data['return']
    ax.scatter(beta_i, ret_i, color=colors[name], s=120, zorder=5, marker='D')
    
    # 计算该股票在 SML 上的理论收益与 Alpha
    er_i = rf + beta_i * sml_slope
    alpha_i = ret_i - er_i
    
    # 动态调整标注位置 (如果在 SML 上方则向上标，下方则向下标)
    offset_y = 20 if alpha_i >= 0 else -25
    
    ax.annotate(f"{name}\nβ={beta_i:.2f}, r={ret_i:.1%}\nα={alpha_i:.2%}",
                xy=(beta_i, ret_i),
                xytext=(15, offset_y),
                textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.5),
                fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.9))

# 设置图表格式
ax.set_title('Security Market Line (SML) and Stock Valuation', fontsize=14, fontweight='bold')
ax.set_xlabel('Beta (β)', fontsize=12)
ax.set_ylabel('Expected Return E(R)', fontsize=12)
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.20)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
ax.legend(loc='upper left', fontsize=10, frameon=True)
ax.grid(True, linestyle='--', alpha=0.6)

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 4. 填充并输出 result 字典
# ==========================================
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 供课堂投屏展示/验证
print(f"SML Slope (Market Risk Premium): {result['sml_slope']:.4f}")
print(f"Expected Return at Beta=1.27: {result['er_at_beta_127']:.4f}")
print(f"Figure saved to: {result['figure_path']}")
