import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ── 1. 读取数据 ──────────────────────────────────────────────
df = pd.read_csv('data/market_snapshot_v1.csv')

# 计算基金日收益率（取 fund 列，假设为净值，算 pct_change）
fund_prices = df['fund']
daily_returns = fund_prices.pct_change().dropna()

# ── 2. 参数设置 ──────────────────────────────────────────────
position = 1_000_000          # 头寸 100 万元
confidence_level = 0.95        # 置信水平（可调）
alpha = 1 - confidence_level  # 显著性水平

# ── 3. 计算历史法 VaR ─────────────────────────────────────────
# 日损益序列
daily_pnl = daily_returns * position

# 历史法 VaR：取损益分布的第 alpha 分位数（负值代表损失），取绝对值
var_quantile = daily_pnl.quantile(alpha)
hist_var_95_1d = abs(var_quantile)

print(f"95% 一日历史 VaR = {hist_var_95_1d:,.2f} 元")

# ── 4. 画直方图 ──────────────────────────────────────────────
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(daily_pnl, bins=50, density=True, alpha=0.7,
        edgecolor='black', color='steelblue', label='日损益分布')

# VaR 线（画在损失侧，即负值）
ax.axvline(x=var_quantile, color='red', linestyle='--', linewidth=2,
           label=f'{confidence_level:.0%} 一日历史 VaR = {hist_var_95_1d:,.2f} 元')

ax.set_title(f'日损益直方图与 {confidence_level:.0%} 历史法 VaR', fontsize=14)
ax.set_xlabel('日损益（元）', fontsize=12)
ax.set_ylabel('概率密度', fontsize=12)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()

# ── 5. 保存图片 & 构建输出字典 ───────────────────────────────
os.makedirs('output', exist_ok=True)
figure_path = 'output/hist_var_histogram.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

result = {
    'hist_var_95_1d': round(hist_var_95_1d, 2),
    'figure_path': figure_path
}

print(f"\n结果字典：{result}")
