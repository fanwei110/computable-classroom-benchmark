import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================
# 1. 读取数据并构造日损益
# =========================
# 请根据实际路径调整，此处假设脚本运行目录下存在 data/market_snapshot_v1.csv
data_path = "data/market_snapshot_v1.csv"
df = pd.read_csv(data_path)

# 约定：收益率已是小数形式（0.05 即 5%），直接使用
returns = df["fund"].dropna().astype(float)

# 头寸规模
capital = 1_000_000  # 1,000,000 元
pnl = returns * capital  # 每日损益序列

# =========================
# 2. 参数化计算历史 VaR
# =========================
conf_level = 0.95                # 可调置信水平
alpha = 1 - conf_level           # 左尾概率
q = np.percentile(pnl, 100 * alpha)  # 线性插值经验分位数（numpy 默认）
var_amount = -q                  # VaR 报告为正的损失金额（人民币）

# 存入结果字典
result = {
    "hist_var_95_1d": var_amount,   # 95% 一日历史 VaR
    "figure_path": None
}

# =========================
# 3. 绘制直方图并标注 VaR
# =========================
fig, ax = plt.subplots(figsize=(10, 6))

# 直方图
ax.hist(pnl, bins=50, color="skyblue", edgecolor="black", alpha=0.7)

# VaR 竖线
ax.axvline(x=q, color="red", linestyle="dashed", linewidth=2,
           label=f"{conf_level*100:.0f}% 1-Day Hist VaR: ¥{var_amount:,.2f}")

# 标签与标题
ax.set_xlabel("Daily P&L (RMB)")
ax.set_ylabel("Frequency")
ax.set_title(f"Daily P&L Distribution and {conf_level*100:.0f}% Historical VaR")
ax.legend()

# =========================
# 4. 保存图形并记录路径
# =========================
fig_path = "var_hist.png"
fig.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.close(fig)  # 释放内存

result["figure_path"] = os.path.abspath(fig_path)

# 脚本结束时 result 字典可供教师直接查看
# print(result)  # 若需在控制台查看可取消注释
