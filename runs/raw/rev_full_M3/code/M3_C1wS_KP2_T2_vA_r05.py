import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ==========================================
# 2. 参数化无风险利率与市场期望收益（方便上课调参）
# ==========================================
rf_pct = 2.3   # 无风险利率 rf (%)
rm_pct = 9.4   # 市场期望收益 E(Rm) (%)

# 内部计算统一转换为小数
rf = rf_pct / 100.0
rm = rm_pct / 100.0

# ==========================================
# 3. 计算 SML 斜率与 beta=1.27 处的期望收益
# ==========================================
# SML斜率即为市场风险溢价
sml_slope = rm - rf

# beta = 1.27 对应的期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 1. 画图：SML 与三只股票的标注
# ==========================================
# 生成 beta 数据 (0 到 2)
betas = np.linspace(0, 2, 200)
# 计算 SML 上的期望收益
er_sml = rf + betas * sml_slope

# 三只股票的给定数据 (beta, 期望收益)
stocks = {
    'X': {'beta': 0.62, 'er': 0.081},
    'Y': {'beta': 1.18, 'er': 0.131},
    'Z': {'beta': 1.51, 'er': 0.099}
}

# 创建画布
fig, ax = plt.subplots(figsize=(10, 7))

# 绘制证券市场线 SML
ax.plot(betas, er_sml, label='SML: $E(R_i) = R_f + \\beta_i (E(R_m) - R_f)$', 
        color='royalblue', linewidth=2.5)

# 标出无风险利率和市场组合点
ax.scatter(0, rf, color='black', zorder=5, s=50)
ax.annotate(f'$R_f$ = {rf_pct}%', xy=(0, rf), xytext=(0.05, rf - 0.012),
            arrowprops=dict(arrowstyle='->', color='black'), fontsize=11, fontweight='bold')

ax.scatter(1, rm, color='black', zorder=5, s=50)
ax.annotate(f'$E(R_m)$ = {rm_pct}%', xy=(1, rm), xytext=(1.05, rm - 0.012),
            arrowprops=dict(arrowstyle='->', color='black'), fontsize=11, fontweight='bold')

# 标出三只股票的点，并计算和画出偏离 SML 的 Alpha
for name, data in stocks.items():
    beta_i = data['beta']
    er_i = data['er']
    
    # 计算该 beta 下 SML 上的定价收益，从而算出 Alpha
    er_i_sml = rf + beta_i * sml_slope
    alpha_i = er_i - er_i_sml
    
    # 根据Alpha正负决定颜色：正Alpha(被低估)为绿色，负Alpha(被高估)为红色
    color = 'seagreen' if alpha_i > 0 else 'crimson'
    
    # 画点
    ax.scatter(beta_i, er_i, color=color, zorder=5, s=70)
    
    # 画 Alpha 偏离虚线
    ax.vlines(beta_i, min(er_i, er_i_sml), max(er_i, er_i_sml), 
              colors=color, linestyles='dashed', linewidth=1.5)
    
    # 标注文字
    offset_y = 0.008 if alpha_i > 0 else -0.015
    ax.annotate(f'{name} ($\\beta$={beta_i}, E(R)={er_i*100:.1f}%)\n$\\alpha$={alpha_i*100:.2f}%',
                xy=(beta_i, er_i), xytext=(beta_i + 0.08, er_i + offset_y),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5), 
                fontsize=10, color=color, fontweight='bold')

# 标出 beta=1.27 处的期望收益计算点
ax.scatter(beta_target, er_at_beta_127, color='darkviolet', marker='*', s=200, zorder=5, 
           label=f'$\\beta=1.27, E(R)={er_at_beta_127*100:.2f}%$')
ax.vlines(beta_target, 0, er_at_beta_127, colors='darkviolet', linestyles='dotted', linewidth=1)
ax.hlines(er_at_beta_127, 0, beta_target, colors='darkviolet', linestyles='dotted', linewidth=1)

# 设置坐标轴与格式
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.16)
ax.set_xlabel('Beta ($\\beta$)', fontsize=12)
ax.set_ylabel('Expected Return $E(R)$', fontsize=12)
ax.set_title('CAPM & Security Market Line (SML)', fontsize=14, fontweight='bold')
ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=1))
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, linestyle='--', alpha=0.6)

# ==========================================
# 4. 保存图形并填充 result 字典
# ==========================================
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 严格按照输出契约构建字典
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 课堂投屏辅助打印（可选，便于当堂核对）
print(f">>> SML 斜率 (市场风险溢价): {result['sml_slope']:.4f} ({result['sml_slope']*100:.2f}%)")
print(f">>> Beta=1.27 对应的期望收益: {result['er_at_beta_127']:.4f} ({result['er_at_beta_127']*100:.2f}%)")
print(f">>> 图形已保存至: {result['figure_path']}")
