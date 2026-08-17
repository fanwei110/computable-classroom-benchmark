#!/usr/bin/env python3
"""
证券市场线 (SML) 与 CAPM 演示
──────────────────────────────────
无风险利率 Rf、市场期望收益 E(Rm) 均为可调参数。
绘制 SML，标注三只股票，报告斜率及 β=1.27 处期望收益。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ============================================================
# 1. 可调参数
# ============================================================
Rf    = 2.3    # 无风险利率 (%)
E_Rm  = 9.4    # 市场期望收益 (%)

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 8.1},
    'Y': {'beta': 1.18, 'return': 13.1},
    'Z': {'beta': 1.51, 'return': 9.9},
}

beta_target = 1.27   # 需要查询的目标 beta

# ============================================================
# 2. 核心计算
# ============================================================
# SML 斜率 = 市场风险溢价
sml_slope = E_Rm - Rf  # 7.1%

# beta=1.27 处 CAPM 期望收益
er_at_beta_127 = Rf + beta_target * sml_slope  # 11.317%

# 计算每只股票的 CAPM 期望收益与 alpha
for name, data in stocks.items():
    data['er_capm'] = Rf + data['beta'] * sml_slope
    data['alpha']   = data['return'] - data['er_capm']

# ============================================================
# 3. 绘图
# ============================================================
mpl.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
mpl.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(11, 7))

# —— SML 线 ——
betas = np.linspace(0, 2, 300)
sml_returns = Rf + betas * sml_slope

ax.plot(betas, sml_returns, 'b-', linewidth=2.5, label='证券市场线 (SML)', zorder=2)

# —— 无风险利率点 ——
ax.plot(0, Rf, 'ko', markersize=9, zorder=4)
ax.annotate(f'无风险利率\nRf = {Rf}%', xy=(0, Rf),
            xytext=(0.10, Rf - 1.4), fontsize=9, ha='left',
            arrowprops=dict(arrowstyle='->', color='black', lw=1))

# —— 市场组合点 ——
ax.plot(1, E_Rm, 'ko', markersize=9, zorder=4)
ax.annotate(f'市场组合 M\n(β=1, E(R)={E_Rm}%)', xy=(1, E_Rm),
            xytext=(1.10, E_Rm + 0.3), fontsize=9, ha='left',
            arrowprops=dict(arrowstyle='->', color='black', lw=1))

# —— 三只股票 ——
colors  = {'X': '#e74c3c', 'Y': '#27ae60', 'Z': '#8e44ad'}
markers = {'X': 'o',        'Y': 's',        'Z': '^'}

# 手动调整标注偏移以避免重叠
annot_offset = {
    'X': (0.07, -1.6),
    'Y': (0.07,  0.6),
    'Z': (0.07, -1.6),
}

for name, data in stocks.items():
    beta_i   = data['beta']
    ret_i    = data['return']
    alpha_i  = data['alpha']
    er_capm  = data['er_capm']

    # 股票实际点
    ax.plot(beta_i, ret_i, marker=markers[name], color=colors[name],
            markersize=12, markeredgecolor='black', markeredgewidth=0.8,
            linestyle='None', zorder=5,
            label=f'股票{name} (β={beta_i}, R={ret_i}%, α={alpha_i:+.2f}%)')

    # 在 SML 上对应的 CAPM 期望点（虚线连接）
    ax.plot(beta_i, er_capm, 'o', color=colors[name], markersize=7,
            alpha=0.45, zorder=3)
    ax.plot([beta_i, beta_i], [min(ret_i, er_capm), max(ret_i, er_capm)],
            '--', color=colors[name], linewidth=1.2, alpha=0.6, zorder=3)

    # 标注
    ox, oy = annot_offset[name]
    label_text = f'{name}: β={beta_i}, R={ret_i}%\nα = {alpha_i:+.2f}%'
    ax.annotate(label_text, xy=(beta_i, ret_i),
                xytext=(beta_i + ox, ret_i + oy), fontsize=9, ha='left',
                arrowprops=dict(arrowstyle='->', color=colors[name], lw=1.2),
                bbox=dict(boxstyle='round,pad=0.35', facecolor='#fffde7',
                          edgecolor=colors[name], alpha=0.9))

# —— β=1.27 查询点 ——
ax.plot(beta_target, er_at_beta_127, 'D', color='darkorange',
        markersize=10, markeredgecolor='black', markeredgewidth=0.8,
        zorder=5, label=f'β={beta_target}: E(R)={er_at_beta_127:.2f}%')
ax.axvline(x=beta_target, color='darkorange', linewidth=0.8, linestyle=':', alpha=0.5)
ax.annotate(f'β = {beta_target}\nE(R) = {er_at_beta_127:.2f}%',
            xy=(beta_target, er_at_beta_127),
            xytext=(beta_target - 0.38, er_at_beta_127 + 1.8), fontsize=9, ha='center',
            arrowprops=dict(arrowstyle='->', color='darkorange', lw=1.2),
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#fff3e0',
                      edgecolor='darkorange', alpha=0.9))

# —— 填充 alpha 区域示意（以股票 Z 为例，负 alpha） ——
ax.fill_between([0, 2], sml_returns, alpha=0.03, color='blue')

# —— 装饰 ——
ax.set_xlabel('Beta (β)', fontsize=13)
ax.set_ylabel('期望收益 E(R)  (%)', fontsize=13)
ax.set_title(f'证券市场线 (SML)  —  CAPM 演示\n'
             f'Rf = {Rf}%,  E(Rm) = {E_Rm}%,  '
             f'斜率 = E(Rm)−Rf = {sml_slope:.1f}%',
             fontsize=14, fontweight='bold')
ax.set_xlim(0, 2)
ax.set_ylim(0, 20)
ax.set_xticks(np.arange(0, 2.1, 0.2))
ax.set_yticks(np.arange(0, 21, 2))
ax.grid(True, alpha=0.25, linestyle='--')
ax.legend(fontsize=9, loc='upper left', framealpha=0.9)

plt.tight_layout()

# ============================================================
# 4. 保存图形
# ============================================================
figure_path = 'sml_capm_plot.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ============================================================
# 5. 控制台输出
# ============================================================
print("=" * 50)
print("CAPM / SML 计算结果")
print("=" * 50)
print(f"无风险利率 Rf          = {Rf}%")
print(f"市场期望收益 E(Rm)     = {E_Rm}%")
print(f"SML 斜率 E(Rm)−Rf      = {sml_slope:.2f}%")
print(f"β = {beta_target} 处 CAPM 期望收益 = {er_at_beta_127:.4f}%")
print("-" * 50)
print("各股票 Alpha 分析:")
for name, data in stocks.items():
    status = "被低估 ✓" if data['alpha'] > 0 else "被高估 ✗"
    print(f"  股票{name}: β={data['beta']}, R={data['return']}%, "
          f"E(R)_CAPM={data['er_capm']:.2f}%, "
          f"α={data['alpha']:+.4f}%  → {status}")
print("=" * 50)

# ============================================================
# 6. 填充结果字典（输出契约）
# ============================================================
result = {
    'sml_slope':      round(sml_slope, 4),
    'er_at_beta_127': round(er_at_beta_127, 4),
    'figure_path':    figure_path,
}

print("\nresult =", result)
