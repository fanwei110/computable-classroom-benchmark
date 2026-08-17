import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------- 参数 ----------
DATA_FILE = "data/market_snapshot_v1.csv"
POSITION = 1_000_000          # 头寸 100 万
CONFIDENCE = 0.95             # 置信度（可调）
TRADING_DAYS = 252

# ---------- 1. 读取数据 ----------
df = pd.read_csv(DATA_FILE, parse_dates=['date'] if 'date' in pd.read_csv(DATA_FILE, nrows=0).columns else False)
# 如果有日期列，按日期排序（确保收益率按时间顺序，但对历史法无严格要求）
if 'date' in df.columns:
    df = df.sort_values('date')

# ---------- 2. 计算日收益率（小数） ----------
price = df['fund']
returns = price.pct_change().dropna()      # 简单收益率（小数）

# ---------- 3. 损益序列 ----------
# 头寸价值变化 = 头寸 × 收益率
pnl = POSITION * returns

# 损失金额 = -损益（损失为正）
losses = -pnl

# ---------- 4. 历史法 VaR ----------
# 取 (CONFIDENCE) 分位数，例如 95% → 0.95 分位数，表示有 5% 的日子损失超过该值
var_95 = losses.quantile(CONFIDENCE)

# 记录结果
hist_var_95_1d = round(var_95, 2)   # 保留两位小数

# ---------- 5. 画图并保存 ----------
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(pnl, bins=50, color='skyblue', edgecolor='white', alpha=0.7)
# VaR 线在损益图上对应 -VaR 的位置
ax.axvline(-var_95, color='red', linestyle='dashed', linewidth=2,
           label=f'Hist VaR 95% 1d: {hist_var_95_1d:,.2f}')
ax.set_title('Daily P&L Histogram with Historical VaR (95% 1-day)')
ax.set_xlabel('Daily P&L')
ax.set_ylabel('Frequency')
ax.legend()

figure_path = "hist_var_plot.png"
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ---------- 6. 输出字典 ----------
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': str(Path(figure_path).resolve())
}

# 打印结果
print(result)
