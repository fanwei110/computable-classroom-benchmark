import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# ── 参数 ──
position = 1_000_000          # 头寸 100万
confidence = 0.95             # 置信度（可调）
var_horizon = 1               # 1日

# ── 1. 读取数据 ──
df = pd.read_csv('data/market_snapshot_v1.csv')
# 取 fund 列日收益率（如果本身已是收益率直接用；如果是净值则先算日收益）
fund_series = df['fund']

# 判断是否为净值序列：若值大部分>1，则视为净值，计算日收益率
if fund_series.median() > 1.5:
    daily_returns = fund_series.pct_change().dropna().values
else:
    daily_returns = fund_series.dropna().values

# ── 2. 损益 = 日收益率 × 头寸 ──
pnl = daily_returns * position

# ── 3. 历史法 VaR ──
# VaR = -percentile(PnL, (1-confidence)×100)  即左尾分位数取负
var_value = -np.percentile(pnl, (1 - confidence) * 100)
# 若需缩放至 var_horizon 天：var_value * sqrt(var_horizon)，这里 horizon=1 不变
var_value_horizon = var_value * np.sqrt(var_horizon)

# ── 4. 绘制损益直方图 + VaR标根线 ──
fig, ax = plt.subplots(figsize=(10, 6))

n, bins, patches = ax.hist(pnl, bins=60, color='steelblue', edgecolor='white', alpha=0.85)

# VaR 竖线
ax.axvline(x=-var_value_horizon, color='red', linestyle='--', linewidth=2,
           label=f'{int(confidence*100)}% 1-Day VaR = {var_value_horizon:,.2f}')

# 将 VaR 左侧柱子标红
for patch, left_edge in zip(patches, bins[:-1]):
    if left_edge < -var_value_horizon:
        patch.set_facecolor('salmon')

ax.set_title(f'历史法 VaR — 损益直方图（头寸 ¥{position:,.0f}，置信度 {confidence*100:.0f}%）',
             fontsize=14)
ax.set_xlabel('损益 (¥)', fontsize=12)
ax.set_ylabel('频数', fontsize=12)
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
fig_path = 'hist_var_pnl_histogram.png'
fig.savefig(fig_path, dpi=150)
plt.close()

# ── 5. 输出 ──
result = {
    'hist_var_95_1d': round(var_value_horizon, 2),
    'figure_path': fig_path
}

print(f"样本数: {len(pnl)}")
print(f"95% 1日历史法VaR: ¥{result['hist_var_95_1d']:,.2f}")
print(f"图片已保存: {result['figure_path']}")
