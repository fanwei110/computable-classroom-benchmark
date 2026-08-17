import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------- 参数 ----------------------------
DATA_PATH = "data/market_snapshot_v1.csv"   # 数据文件路径
POSITION = 1_000_000.0                     # 头寸金额（人民币）
CONFIDENCE_LEVEL = 0.95                    # 置信水平（可调参数）
ALPHA = 1 - CONFIDENCE_LEVEL               # 左尾概率
FIGURE_PATH = "var_histogram.png"          # 输出图形路径

# ---------------------------- 1. 读取数据并构造日损益 ----------------------------
# 读取CSV，假设包含"fund"列，表示日收益率（小数形式，如0.01表示1%）
df = pd.read_csv(DATA_PATH)
returns = df["fund"].dropna().values       # 日收益序列，剔除缺失值

# 日损益 = 头寸 × 收益率
profit_loss = POSITION * returns

# ---------------------------- 2. 计算历史VaR ----------------------------
# 经验分布左尾分位数（即损益的alpha分位数）
var_threshold = np.quantile(profit_loss, ALPHA)
# 在险价值通常定义为损失的正值，即负分位数的绝对值（若分位数为负）
hist_var_95_1d = -var_threshold

# ---------------------------- 3. 绘制直方图并标注VaR ----------------------------
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制日损益直方图
ax.hist(profit_loss, bins=50, color='skyblue', edgecolor='black', alpha=0.7)

# 添加VaR竖线
ax.axvline(x=var_threshold, color='red', linestyle='--', linewidth=2,
           label=f'{CONFIDENCE_LEVEL*100:.0f}% 1-Day Hist VaR: ¥{hist_var_95_1d:,.2f}')

# 标注
ax.set_xlabel('Daily Profit / Loss (CNY)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title(f'Distribution of Daily P&L (Position = ¥{POSITION:,.0f})', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

# 在VaR线附近添加文字标注（避免与图例重叠）
ymin, ymax = ax.get_ylim()
ax.text(var_threshold, ymax * 0.9,
        f'  VaR = ¥{hist_var_95_1d:,.2f}',
        color='red', fontsize=11, va='top')

plt.tight_layout()
fig.savefig(FIGURE_PATH, dpi=150)
plt.close(fig)

# ---------------------------- 4. 结果输出 ----------------------------
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': FIGURE_PATH
}

# 打印结果以便教师查看
print("===== 计算结果 =====")
print(f"95% 一日历史 VaR (人民币): ¥{hist_var_95_1d:,.2f}")
print(f"图形已保存至: {FIGURE_PATH}")
print("result 字典内容:", result)
