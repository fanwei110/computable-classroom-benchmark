import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------ 可调参数 ------------------------------
POSITION_VALUE = 1_000_000.0       # 头寸金额（人民币）
CONFIDENCE_LEVEL = 0.95            # 置信水平（可改为 0.99 等）
# ---------------------------------------------------------------------

# 1. 读取数据，提取日收益序列
DATA_PATH = "data/market_snapshot_v1.csv"
df = pd.read_csv(DATA_PATH)
raw_returns = df["fund"].dropna().values.astype(float)

# 自动处理收益率格式：若数值较大（如百分比形式）则转换为小数
if np.max(np.abs(raw_returns)) > 0.5:
    # 假设为百分比收益率，例如 0.5 表示 0.5%
    daily_returns = raw_returns / 100.0
else:
    daily_returns = raw_returns

# 2. 构造头寸日损益序列
pnl = POSITION_VALUE * daily_returns   # 日损益（人民币）

# 3. 由经验分布计算历史 VaR
alpha = CONFIDENCE_LEVEL
percentile_point = 100 * (1 - alpha)           # 例如 95% 对应 5% 分位数
var_loss = -np.percentile(pnl, percentile_point)  # 正的人民币损失金额
loss_threshold = -var_loss                     # 损益分布中的负分位点（作图用）

# 4. 绘制直方图并标出 VaR
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(pnl, bins=60, color="steelblue", edgecolor="white", alpha=0.8,
        label="Daily PnL distribution")
ax.axvline(x=loss_threshold, color="firebrick", linestyle="--", linewidth=2.5,
           label=f"{int(alpha*100)}% Historical VaR: ¥{var_loss:,.2f}")
ax.set_xlabel("Daily Profit & Loss (CNY)", fontsize=12)
ax.set_ylabel("Frequency", fontsize=12)
ax.set_title(f"Daily PnL Distribution with {int(alpha*100)}% VaR", fontsize=14)
ax.legend(fontsize=11)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()

# 5. 保存图形
FIGURE_PATH = "var_histogram.png"
fig.savefig(FIGURE_PATH, dpi=150, bbox_inches="tight")
plt.close(fig)

# 6. 输出契约
result = {
    "hist_var_95_1d": var_loss,   # 95% 一日历史 VaR（人民币）
    "figure_path": FIGURE_PATH    # 图形文件路径
}

# 在课堂投屏时打印确认
print("=== 计算结果 ===")
print(f"95% 一日历史 VaR = ¥{var_loss:,.2f}")
print(f"图形已保存至：{FIGURE_PATH}")
print(f"result 字典：{result}")
