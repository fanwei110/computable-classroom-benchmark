import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# 参数设置（置信水平可调）
# ============================================================
confidence_level = 0.95          # 可调置信水平
position = 1_000_000            # 头寸 100 万元
alpha = 1 - confidence_level    # 显著性水平

# ============================================================
# 1. 读取数据
# ============================================================
df = pd.read_csv('data/market_snapshot_v1.csv')
fund = df['fund']

# 计算日收益率（ pct_change 即 (P_t - P_{t-1}) / P_{t-1} ）
daily_returns = fund.pct_change().dropna()

# 日损益 = 头寸 × 日收益率
daily_pnl = position * daily_returns

# ============================================================
# 2. 历史模拟法 VaR
# ============================================================
# 对损益排序，取 alpha 分位数（左侧尾部）
var_quantile = daily_pnl.quantile(alpha)
# VaR 报告为正的损失金额
hist_var = -var_quantile

print(f"基金日收益率样本数: {len(daily_returns)}")
print(f"日收益率均值: {daily_returns.mean():.6f}")
print(f"日收益率标准差(ddof=1): {daily_returns.std(ddof=1):.6f}")
print(f"{confidence_level*100:.0f}% 一日历史 VaR (损失金额): {hist_var:,.2f} 元")

# ============================================================
# 3. 画日损益直方图 + VaR 线
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))

# 直方图
ax.hist(daily_pnl, bins=60, edgecolor='black', alpha=0.7, color='steelblue')

# VaR 线：画在 alpha 分位数位置（左侧尾部）
ax.axvline(x=var_quantile, color='red', linestyle='--', linewidth=2,
           label=f'{confidence_level*100:.0f}% 1-day Hist VaR = {hist_var:,.0f} 元')

ax.set_xlabel('日损益（元）', fontsize=12)
ax.set_ylabel('频数', fontsize=12)
ax.set_title(f'日损益直方图  |  头寸 = {position/1e6:.0f} 百万元  |  '
             f'{confidence_level*100:.0f}% 一日历史 VaR', fontsize=13)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()

# 保存图表
os.makedirs('output', exist_ok=True)
figure_path = 'output/hist_var_pnl_histogram.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ============================================================
# 4. 输出契约
# ============================================================
result = {
    'hist_var_95_1d': hist_var,
    'figure_path': figure_path
}

print(f"\n结果字典 result = {result}")
