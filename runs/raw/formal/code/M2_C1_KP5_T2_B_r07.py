import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- 读取数据 ----------
df = pd.read_csv('data/market_snapshot_v1.csv')
returns = df['fund']        # 假设已是日收益率（小数）

# 若您的 fund 列是价格，请使用:
# returns = df['fund'].pct_change().dropna()

# ---------- 参数设置 ----------
position = 1_000_000        # 头寸 100 万
conf_level = 0.95           # 置信度（可调）
pnl = position * returns    # 每日损益

# ---------- 历史法 VaR ----------
var_cutoff = np.percentile(pnl, 100 * (1 - conf_level))  # 5%分位数
var_95_1d = -var_cutoff      # 报告为正的损失金额

# ---------- 画直方图并标线 ----------
plt.figure(figsize=(8, 5))
plt.hist(pnl, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(var_cutoff, color='red', linestyle='dashed', linewidth=2,
            label=f'95% 1-Day VaR: {var_95_1d:,.2f}')
plt.legend()
plt.title('Historical Simulation PnL Distribution')
plt.xlabel('Profit & Loss')
plt.ylabel('Frequency')
plt.tight_layout()

fig_path = 'var_histogram.png'
plt.savefig(fig_path)
plt.close()

# ---------- 输出契约 ----------
result = {
    'hist_var_95_1d': var_95_1d,
    'figure_path': fig_path
}
print(result)
