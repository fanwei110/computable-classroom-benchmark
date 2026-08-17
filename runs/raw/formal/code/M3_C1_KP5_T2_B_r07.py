import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ============ 可调参数 ============
confidence_level = 0.95       # 置信度，可改为 0.99 等
position = 1_000_000          # 头寸（元）
holding_period = 1            # 持有期（日）

# ============ 读取数据 ============
df = pd.read_csv('data/market_snapshot_v1.csv')
daily_returns = df['fund'].dropna().values

# ============ 计算损益 ============
pnl = daily_returns * position  # 日损益序列

# ============ 历史法 VaR ============
alpha = 1 - confidence_level
# VaR 取损益分布的 alpha 分位数（左尾），取绝对值报告
var_quantile = np.percentile(pnl, alpha * 100)
var_value = -var_quantile  # 报告为正数

# ============ 绘图 ============
fig, ax = plt.subplots(figsize=(10, 6))

# 直方图
counts, bins, patches = ax.hist(pnl, bins=80, edgecolor='white',
                                 alpha=0.75, color='steelblue',
                                 label='日损益分布')

# VaR 竖线
ax.axvline(x=var_quantile, color='red', linestyle='--', linewidth=2,
           label=f'{confidence_level*100:.0f}% 1日VaR = {var_value:,.2f} 元')

ax.set_title(f'历史法VaR  |  头寸 {position/1e6:.0f}万  |  置信度 {confidence_level*100:.0f}%  |  持有期 {holding_period}日',
             fontsize=13)
ax.set_xlabel('损益（元）')
ax.set_ylabel('频数')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()

# ============ 保存图片 ============
os.makedirs('output', exist_ok=True)
fig_path = 'output/hist_var_pnl_histogram.png'
fig.savefig(fig_path, dpi=150)
plt.close()

# ============ 输出契约 ============
result = {
    'hist_var_95_1d': round(var_value, 2),
    'figure_path': fig_path
}

print(f"95% 1日历史法VaR: {var_value:,.2f} 元")
print(f"图片已保存至: {fig_path}")
print(result)
