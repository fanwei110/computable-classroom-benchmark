import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# 可调参数
# ========================
CONFIDENCE_LEVEL = 0.95          # 置信水平（可调）
POSITION = 1_000_000             # 头寸（人民币）
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'var_histogram.png'

# ========================
# 1. 读取数据并构造日损益
# ========================
# 假设 CSV 中包含 'fund' 列，为日简单收益率（小数形式，如 0.01 表示 1%）
df = pd.read_csv(DATA_PATH)
returns = df['fund'].dropna().to_numpy()   # 剔除缺失值

# 若实际数据是百分数形式（如 1 表示 1%），可在此取消注释以自动缩放
# if np.nanmax(np.abs(returns)) > 0.5:   # 经验判断：最大绝对值超过0.5则视为百分数
#     returns = returns / 100.0

# 日损益 = 头寸 × 日收益率
pnl = POSITION * returns

# ========================
# 2. 计算历史 VaR（经验分位数）
# ========================
var_cutoff = np.percentile(pnl, 100 * (1 - CONFIDENCE_LEVEL))  # 左尾分位数（负值）
var_value = -var_cutoff   # VaR 通常以正数表示损失金额

# ========================
# 3. 绘制损益直方图并标记 VaR
# ========================
plt.figure(figsize=(10, 5))
plt.hist(pnl, bins=50, color='steelblue', edgecolor='white', alpha=0.8)
plt.axvline(var_cutoff, color='red', linestyle='--', linewidth=2,
            label=f"VaR {CONFIDENCE_LEVEL*100:.0f}%: ¥{var_value:,.2f}")

plt.title(f"Historical Daily P&L Distribution (Position = ¥{POSITION:,.0f})")
plt.xlabel("Profit / Loss (CNY)")
plt.ylabel("Frequency")
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(FIGURE_PATH, dpi=150)
plt.close()

# ========================
# 4. 整理输出
# ========================
result = {
    'hist_var_95_1d': round(var_value, 2),
    'figure_path': FIGURE_PATH
}

print("计算完成，结果如下：")
print(result)
