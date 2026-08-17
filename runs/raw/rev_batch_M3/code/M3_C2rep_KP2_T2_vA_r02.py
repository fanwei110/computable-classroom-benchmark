#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
证券投资学 — CAPM 与证券市场线 (SML) 演示
画出 SML，标注三只股票，报告斜率与指定 beta 处的期望收益。
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

# ────────────────────────── 参数设定 ──────────────────────────
rf  = 0.023          # 无风险利率 2.3%
rm  = 0.094          # 市场期望收益 9.4%

# 三只股票: (名称, beta, 实际收益)
stocks = [
    ("X", 0.62, 0.081),
    ("Y", 1.18, 0.131),
    ("Z", 1.51, 0.099),
]

# ────────────────────────── 核心计算 ──────────────────────────
def capm_expected_return(beta, rf, rm):
    """SML: E(R_i) = r_f + β_i × (E(R_m) - r_f)"""
    return rf + beta * (rm - rf)

sml_slope = rm - rf                           # SML 斜率
er_at_beta_127 = capm_expected_return(1.27, rf, rm)  # beta=1.27 处的 CAPM 期望收益

# ────────────────────────── 绘图 ──────────────────────────────
# 中文字体设置（兼容多平台）
matplotlib.rcParams["font.sans-serif"] = [
    "SimHei", "Microsoft YaHei", "WenQuanYi Micro Hei",
    "Arial Unicode MS", "DejaVu Sans"
]
matplotlib.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(10, 6.5))

# 1. 画 SML
beta_range = np.linspace(0, 2, 300)
sml_returns = capm_expected_return(beta_range, rf, rm)
ax.plot(beta_range, sml_returns * 100, "b-", linewidth=2.2, label="证券市场线 (SML)")

# 2. 标出无风险资产与市场组合
ax.plot(0, rf * 100, "ko", markersize=8, zorder=5)
ax.annotate(f"无风险资产\n(0, {rf*100:.1f}%)", xy=(0, rf*100),
            xytext=(0.12, rf*100 - 1.0), fontsize=9,
            arrowprops=dict(arrowstyle="->", color="gray"))

ax.plot(1, rm * 100, "k^", markersize=9, zorder=5)
ax.annotate(f"市场组合\n(1, {rm*100:.1f}%)", xy=(1, rm*100),
            xytext=(1.12, rm*100 + 0.5), fontsize=9,
            arrowprops=dict(arrowstyle="->", color="gray"))

# 3. 标出三只股票（带 alpha 注释）
colors = {"X": "#e74c3c", "Y": "#2ecc71", "Z": "#9b59b6"}
for name, beta_i, ret_i in stocks:
    er_i = capm_expected_return(beta_i, rf, rm)
    alpha_i = ret_i - er_i
    # 股票点
    ax.plot(beta_i, ret_i * 100, "o", color=colors[name], markersize=10,
            markeredgecolor="black", markeredgewidth=0.8, zorder=6,
            label=f"股票 {name} (β={beta_i}, R={ret_i*100:.1f}%, α={alpha_i*100:+.2f}%)")
    # SML 上对应点（用虚线连接）
    ax.plot([beta_i, beta_i], [er_i * 100, ret_i * 100],
            "--", color=colors[name], linewidth=1.2, alpha=0.7)
    ax.plot(beta_i, er_i * 100, "s", color=colors[name], markersize=6,
            markeredgecolor="black", markeredgewidth=0.5, alpha=0.6, zorder=5)
    # 标注
    offset_y = 1.2 if alpha_i >= 0 else -1.5
    ax.annotate(name, xy=(beta_i, ret_i * 100),
                xytext=(beta_i + 0.06, ret_i * 100 + offset_y),
                fontsize=12, fontweight="bold", color=colors[name])

# 4. beta=1.27 处的期望收益标记
er_127 = capm_expected_return(1.27, rf, rm)
ax.axvline(x=1.27, color="gray", linestyle=":", linewidth=0.9, alpha=0.5)
ax.plot(1.27, er_127 * 100, "D", color="darkorange", markersize=8,
        markeredgecolor="black", markeredgewidth=0.8, zorder=6)
ax.annotate(f"β=1.27\nE(R)={er_127*100:.2f}%", xy=(1.27, er_127*100),
            xytext=(1.38, er_127*100 + 1.5), fontsize=9, color="darkorange",
            arrowprops=dict(arrowstyle="->", color="darkorange"))

# 5. 填充合理定价区域（可选视觉增强）
ax.fill_between(beta_range, (rf + beta_range * (rm - rf)) * 100 - 0.15,
                (rf + beta_range * (rm - rf)) * 100 + 0.15,
                alpha=0.08, color="blue")

# 6. 图形装饰
ax.set_xlabel("β (Beta)", fontsize=12)
ax.set_ylabel("期望收益率 (%)", fontsize=12)
ax.set_title(f"证券市场线 (SML)\n"
             f"$r_f$ = {rf*100:.1f}%,  $E(R_m)$ = {rm*100:.1f}%,  "
             f"SML 斜率 = {sml_slope*100:.1f}%",
             fontsize=13, fontweight="bold")
ax.set_xlim(0, 2)
ax.set_ylim(0, 20)
ax.legend(loc="upper left", fontsize=8.5, framealpha=0.9)
ax.grid(True, alpha=0.3)

# 添加文字说明
textstr = (f"SML: E(R) = {rf*100:.1f}% + β × {sml_slope*100:.1f}%\n"
           f"β=1.27 处 E(R) = {er_127*100:.2f}%")
props = dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.85, edgecolor="gray")
ax.text(0.02, 0.97, textstr, transform=ax.transAxes, fontsize=9.5,
        verticalalignment="top", bbox=props)

plt.tight_layout()

# ────────────────────────── 保存图形 ──────────────────────────
figure_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sml_plot.png")
fig.savefig(figure_path, dpi=150, bbox_inches="tight")
plt.close(fig)

# ────────────────────────── 输出结果 ──────────────────────────
result = {
    "sml_slope": round(sml_slope, 6),            # 0.071
    "er_at_beta_127": round(er_at_beta_127, 6),   # 0.11317
    "figure_path": figure_path,
}

print("=" * 55)
print("CAPM 证券市场线 (SML) 计算结果")
print("=" * 55)
print(f"  无风险利率 rf          = {rf*100:.1f}%")
print(f"  市场期望收益 rm        = {rm*100:.1f}%")
print(f"  SML 斜率 (rm - rf)     = {sml_slope*100:.1f}%  ({sml_slope:.6f})")
print(f"  β=1.27 处 CAPM 期望收益 = {er_127*100:.2f}%  ({er_127:.6f})")
print("-" * 55)
for name, beta_i, ret_i in stocks:
    er_i = capm_expected_return(beta_i, rf, rm)
    alpha_i = ret_i - er_i
    status = "被低估(α>0)" if alpha_i > 0 else "被高估(α<0)"
    print(f"  股票{name}: β={beta_i:.2f}, 实际={ret_i*100:.1f}%, "
          f"SML={er_i*100:.2f}%, α={alpha_i*100:+.2f}%  [{status}]")
print("-" * 55)
print(f"  图形已保存至: {figure_path}")
print("=" * 55)
print(f"\nresult = {result}")
