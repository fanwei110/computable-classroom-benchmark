import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ============================================================
# 参数（置信水平可调）
# ============================================================
POSITION = 1_000_000          # 头寸（人民币）
CONFIDENCE_LEVEL = 0.95       # 置信水平，可调参数
FIGURE_PATH = "var_histogram.png"

# ============================================================
# Step 1: 读取快照 CSV，构造头寸的日损益
# ============================================================
df = pd.read_csv("data/market_snapshot_v1.csv")
daily_returns = df["fund"].values          # 日收益率序列
daily_pnl = POSITION * daily_returns       # 日损益（人民币）

# ============================================================
# Step 2: 由经验分布计算历史 VaR（人民币）
# ============================================================
# VaR_α = - Quantile_{1-α}(P&L)
# 95% 置信水平下，取 P&L 分布的第 5 分位数，取负即为 VaR
alpha = CONFIDENCE_LEVEL
pnl_quantile = np.quantile(daily_pnl, 1 - alpha)   # 损益分布的左尾分位数
hist_var = -pnl_quantile                           # VaR 报告为正数

# ============================================================
# Step 3: 画直方图并加带标注的 VaR 线
# ============================================================
fig, ax = plt.subplots(figsize=(11, 6))

# 直方图
n_bins = 50
ax.hist(daily_pnl, bins=n_bins, edgecolor="black", alpha=0.72,
        color="steelblue", label="日损益分布")

# VaR 竖线：位于 P&L = -VaR 处（即左尾分位数位置）
var_line_x = -hist_var  # 等价于 pnl_quantile
ax.axvline(x=var_line_x, color="red", linestyle="--", linewidth=2.2,
           label=f"{alpha*100:.0f}% 历史 VaR")

# 在竖线旁加文本标注，标明 VaR 数值
y_top = ax.get_ylim()[1]
ax.annotate(
    f"VaR = ¥{hist_var:,.2f}\n(损失分位数)",
    xy=(var_line_x, y_top * 0.55),
    xytext=(var_line_x - (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.22,
            y_top * 0.75),
    fontsize=11, color="red", fontweight="bold",
    arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="red", alpha=0.85)
)

# 格式美化
ax.set_xlabel("日损益（人民币 ¥）", fontsize=13)
ax.set_ylabel("频数", fontsize=13)
ax.set_title(f"日损益分布直方图  &  {alpha*100:.0f}% 一日历史 VaR\n"
             f"头寸 = ¥{POSITION:,.0f}", fontsize=14)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"¥{x:,.0f}"))
ax.legend(fontsize=11, loc="upper right")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()

# ============================================================
# Step 4: 保存图形并填充 result
# ============================================================
fig.savefig(FIGURE_PATH, dpi=150, bbox_inches="tight")
plt.close(fig)

result = {
    "hist_var_95_1d": hist_var,   # 95% 一日历史 VaR（人民币）
    "figure_path": FIGURE_PATH
}

# ---- 运行时输出 ----
print(f"95% 一日历史 VaR = ¥{hist_var:,.2f}")
print(f"图形已保存至: {FIGURE_PATH}")
