import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========================
# 可调参数
# ========================
CONFIDENCE_LEVEL = 0.95          # 置信水平，可修改为 0.99 等
POSITION = 1_000_000.0           # 头寸金额（人民币）
DATA_FILE = "fund_returns.csv"   # 课程数据快照文件，假设包含 'fund' 列
FIGURE_FILE = "var_figure.png"   # 输出图表文件名
BINS = 50                        # 直方图分组数

# ========================
# 1. 读取数据
# ========================
df = pd.read_csv(DATA_FILE)
returns = df["fund"].dropna().to_numpy(dtype=np.float64)

# ========================
# 2. 计算日损益序列
# ========================
pnl = POSITION * returns          # 每日损益（人民币）

# ========================
# 3. 计算历史 VaR
# ========================
# 损益分布的左尾分位数（例如 5% 分位数）
percentile_left = (1 - CONFIDENCE_LEVEL) * 100
var_cutoff = np.percentile(pnl, percentile_left)   # 这里的值为负（损失）
hist_var = -var_cutoff                             # VaR 通常报告为正的损失金额

# ========================
# 4. 画图
# ========================
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=BINS, color="steelblue", edgecolor="white", alpha=0.8)

# 在损益分布的左尾分位数处画竖线，并标注 VaR 值
plt.axvline(x=var_cutoff, color="red", linestyle="--", linewidth=2,
            label=f"{CONFIDENCE_LEVEL*100:.0f}% 1-Day Historical VaR: ¥{hist_var:,.2f}")

plt.title("Daily P&L Distribution and Historical Value-at-Risk", fontsize=14)
plt.xlabel("Daily Profit / Loss (RMB)", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.legend(loc="upper left")
plt.tight_layout()

# 保存图片
plt.savefig(FIGURE_FILE, dpi=150)
plt.close()

# ========================
# 5. 输出结果字典
# ========================
result = {
    "hist_var_95_1d": hist_var,      # 报告 95% 一日历史 VaR（人民币）
    "figure_path": FIGURE_FILE       # 图片保存路径
}

# 为了可复现，可打印结果（根据评分环境决定）
print(result)
