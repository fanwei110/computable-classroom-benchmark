import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# ── 读取数据 ──
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_prices = df['fund']

# 日收益率（简单收益率）
daily_returns = fund_prices.pct_change().dropna()

# ── 参数 ──
position = 1_000_000          # 100万头寸
confidence_level = 0.95       # 置信度（可调）
alpha = 1 - confidence_level  # 尾部概率

# ── 损益序列 ──
pnl = position * daily_returns

# ── 历史法 VaR ──
# 取 P&L 的下 alpha 分位数（负值 = 亏损），VaR 报告为正的损失金额
var_value = -np.percentile(pnl, alpha * 100)

# ── 绘制损益直方图 + VaR 标根线 ──
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(pnl, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
ax.axvline(x=-var_value, color='red', linestyle='--', linewidth=2,
           label=f'{confidence_level*100:.0f}% 1-day VaR = ¥{var_value:,.2f}')
ax.set_xlabel('P&L (¥)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title(f'Historical VaR — P&L Histogram\n'
             f'Position = ¥{position:,}  |  '
             f'{confidence_level*100:.0f}% 1-day VaR = ¥{var_value:,.2f}',
             fontsize=13)
ax.legend(fontsize=11)
plt.tight_layout()

figure_path = 'hist_var_pnl_histogram.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ── 输出契约 ──
result = {
    'hist_var_95_1d': var_value,
    'figure_path': figure_path
}

print(f"95% 1-day Historical VaR = ¥{var_value:,.2f}")
print(f"Figure saved → {figure_path}")
print(result)
