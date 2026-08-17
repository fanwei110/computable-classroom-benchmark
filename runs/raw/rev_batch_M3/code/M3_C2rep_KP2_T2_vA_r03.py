import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ==========================================
# 1. 参数设置 (可调参数)
# ==========================================
rf = 0.023  # 无风险利率 2.3%
rm = 0.094  # 市场期望收益 9.4%

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099},
}

# ==========================================
# 2. 核心计算
# ==========================================
# SML 斜率
sml_slope = rm - rf

# beta = 1.27 处的 CAPM 期望收益
beta_target = 1.27
er_at_beta_127 = rf + beta_target * sml_slope

# ==========================================
# 3. 绘图：证券市场线 (SML) 与股票标注
# ==========================================
# 设置中文字体，以防系统不支持黑体时回退到无中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 7))

# 生成 beta 序列并计算 SML 上的期望收益
betas = np.linspace(0, 2, 100)
sml_returns = rf + betas * sml_slope

# 画出 SML 线
ax.plot(betas, sml_returns * 100, label='证券市场线 (SML)', color='royalblue', linewidth=2.5)

# 画出无风险利率点和市场组合点
ax.scatter(0, rf * 100, color='black', zorder=5)
ax.annotate('无风险利率 $r_f$', (0, rf * 100), textcoords="offset points", xytext=(-15, 10), ha='center', fontsize=10)

ax.scatter(1, rm * 100, color='black', zorder=5)
ax.annotate('市场组合 $r_m$', (1, rm * 100), textcoords="offset points", xytext=(15, -15), ha='center', fontsize=10)

# 遍历股票，画点并标注 Alpha (偏离 SML 的部分)
for name, data in stocks.items():
    beta_s = data['beta']
    actual_r = data['return']
    capm_r = rf + beta_s * sml_slope
    alpha = actual_r - capm_r
    
    # 画出股票实际收益点
    ax.scatter(beta_s, actual_r * 100, color='crimson', zorder=5, s=60)
    
    # 画出从 SML 到实际收益点的垂直虚线 (表示 Alpha)
    ax.plot([beta_s, beta_s], [capm_r * 100, actual_r * 100], color='gray', linestyle='--', linewidth=1.2)
    
    # 标注股票名称和 Alpha 值
    y_offset = 12 if alpha > 0 else -18
    ax.annotate(f"股票 {name}\nAlpha = {alpha*100:.2f}%", 
                (beta_s, actual_r * 100), 
                textcoords="offset points", 
                xytext=(15, y_offset), 
                ha='center', 
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

# 图形格式设置
ax.set_title(f'CAPM 与证券市场线 (SML)\n$r_f$ = {rf*100:.1f}%, $r_m$ = {rm*100:.1f}%, 斜率 = {sml_slope*100:.2f}%', fontsize=14)
ax.set_xlabel('Beta ($\\beta$)', fontsize=12)
ax.set_ylabel('期望收益 (%)', fontsize=12)
ax.set_xlim(0, 2)
ax.set_ylim(0, 16)
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(loc='upper left', fontsize=11)

# 保存图形
figure_path = 'sml_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 4. 结果封装
# ==========================================
result = {
    'sml_slope': sml_slope,
    'er_at_beta_127': er_at_beta_127,
    'figure_path': figure_path
}

# 控制台输出验证
print("=== 计算结果 ===")
print(f"SML 斜率: {result['sml_slope']:.4f} ({result['sml_slope']*100:.2f}%)")
print(f"Beta=1.27 处期望收益: {result['er_at_beta_127']:.4f} ({result['er_at_beta_127']*100:.2f}%)")
print(f"图形已保存至: {result['figure_path']}")
