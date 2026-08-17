"""
自包含脚本：绘制证券市场线 (SML)，标注股票 X/Y/Z，
报告 SML 斜率与 beta=1.27 处的 CAPM 期望收益。
仅依赖 numpy / scipy / pandas / matplotlib，离线可复现。
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")  # 无显示环境下也能保存图片
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# 可调参数（题目给定，但保留为变量便于复用 / 调整）
# ----------------------------------------------------------------------
RISK_FREE_RATE = 2.3   # rf, % 每年
MARKET_EXPECTED_RETURN = 9.4  # E(Rm), % 每年

# 股票数据
STOCKS = {
    "X": {"beta": 0.62, "return": 8.1},
    "Y": {"beta": 1.18, "return": 13.1},
    "Z": {"beta": 1.51, "return": 9.9},
}

# 题目要求的目标 beta
TARGET_BETA = 1.27

# ----------------------------------------------------------------------
# CAPM / SML
# E(R_i) = rf + beta_i * (E(Rm) - rf)
# ----------------------------------------------------------------------
rf = RISK_FREE_RATE
erm = MARKET_EXPECTED_RETURN
sml_slope = erm - rf  # 单位：百分比 / 单位 beta

def capm_expected_return(beta: float, rf: float, erm: float) -> float:
    return rf + beta * (erm - rf)

er_at_beta_127 = capm_expected_return(TARGET_BETA, rf, erm)

# ----------------------------------------------------------------------
# 绘图
# ----------------------------------------------------------------------
betas = np.linspace(0.0, 2.0, 400)
sml_returns = capm_expected_return(betas, rf, erm)

fig, ax = plt.subplots(figsize=(9, 6.2))

# SML 主线
ax.plot(betas, sml_returns, color="#1f4e79", linewidth=2.2, label="SML", zorder=3)

# 市场组合点 (beta=1)
ax.scatter([1.0], [erm], color="black", marker="*", s=220, zorder=6,
           edgecolors="white", linewidths=0.8)
ax.annotate(f"Market\nβ=1, E(R)={erm:.1f}%",
            xy=(1.0, erm), xytext=(1.06, erm - 1.6),
            fontsize=9, color="black")

# 无风险点 (beta=0)
ax.scatter([0.0], [rf], color="black", marker="o", s=60, zorder=6)
ax.annotate(f"Rf\nβ=0, {rf:.1f}%",
            xy=(0.0, rf), xytext=(0.04, rf + 0.4),
            fontsize=9, color="black")

# 三只股票：同时画出 SML 上对应 CAPM 点 (空心) 与实际收益点 (实心)
stock_colors = {"X": "#c0392b", "Y": "#27ae60", "Z": "#8e44ad"}
for name, info in STOCKS.items():
    b = info["beta"]
    r_actual = info["return"]
    r_capm = capm_expected_return(b, rf, erm)
    color = stock_colors[name]

    # CAPM 期望点（SML 上）
    ax.scatter([b], [r_capm], facecolors="white", edgecolors=color,
               linewidths=1.6, s=70, zorder=5)
    # 实际收益点
    ax.scatter([b], [r_actual], color=color, s=85, zorder=7,
               edgecolors="white", linewidths=0.8)

    # 用虚线连接两点，直观显示定价偏离
    ax.plot([b, b], [r_capm, r_actual], color=color, linestyle="--",
            linewidth=1.0, alpha=0.7, zorder=4)

    label = (f"{name}\nβ={b}, R={r_actual}%\n"
             f"CAPM={r_capm:.2f}%")
    # 标注位置自适应：高于 SML 向上偏，低于向下偏
    offset_y = 1.0 if r_actual >= r_capm else -1.6
    ax.annotate(label, xy=(b, r_actual),
                xytext=(b + 0.06, r_actual + offset_y),
                fontsize=9, color=color,
                bbox=dict(boxstyle="round,pad=0.25",
                          fc="white", ec=color, alpha=0.9))

# 目标 beta=1.27 处的 CAPM 期望收益标注
ax.scatter([TARGET_BETA], [er_at_beta_127], color="darkorange",
           marker="D", s=90, zorder=8, edgecolors="white", linewidths=0.8)
ax.annotate(f"β={TARGET_BETA}\nE(R)={er_at_beta_127:.3f}%",
            xy=(TARGET_BETA, er_at_beta_127),
            xytext=(TARGET_BETA - 0.55, er_at_beta_127 + 1.2),
            fontsize=9, color="darkorange",
            arrowprops=dict(arrowstyle="->", color="darkorange", lw=1.0),
            bbox=dict(boxstyle="round,pad=0.25",
                      fc="white", ec="darkorange", alpha=0.9))

# 装饰
ax.set_xlabel("Beta", fontsize=11)
ax.set_ylabel("Expected Return (%)", fontsize=11)
ax.set_title(f"Security Market Line\n"
             f"rf = {rf:.2f}%,  E(Rm) = {erm:.2f}%,  "
             f"SML slope = {sml_slope:.3f}% per unit β",
             fontsize=12)
ax.set_xlim(0, 2)
# y 轴范围略放宽，容纳标注
y_min = min(sml_returns.min(), min(s["return"] for s in STOCKS.values())) - 2
y_max = max(sml_returns.max(), max(s["return"] for s in STOCKS.values())) + 3
ax.set_ylim(y_min, y_max)
ax.grid(True, alpha=0.3)
ax.axhline(rf, color="gray", linestyle=":", linewidth=0.8, alpha=0.6)
ax.legend(loc="upper left", framealpha=0.9)

plt.tight_layout()

# ----------------------------------------------------------------------
# 保存图片
# ----------------------------------------------------------------------
here = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() \
    else os.getcwd()
figure_path = os.path.join(here, "sml_plot.png")
plt.savefig(figure_path, dpi=150, bbox_inches="tight")
plt.close(fig)

# ----------------------------------------------------------------------
# 输出契约
# ----------------------------------------------------------------------
result = {
    "sml_slope": float(sml_slope),           # 单位：%/β
    "er_at_beta_127": float(er_at_beta_127), # 单位：%
    "figure_path": figure_path,
}

if __name__ == "__main__":
    print("result =")
    for k, v in result.items():
        print(f"  {k!r}: {v}")
