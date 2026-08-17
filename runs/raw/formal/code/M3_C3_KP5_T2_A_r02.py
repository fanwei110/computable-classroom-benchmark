import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# ==================== 可调参数 ====================
confidence_level = 0.95          # 置信水平（可调，如 0.99, 0.90 等）
position = 1_000_000            # 头寸：100万元
# ==================================================

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'PingFang SC']
matplotlib.rcParams['axes.unicode_minus'] = False

# ---------- 1. 读取数据 ----------
df = pd.read_csv('data/market_snapshot_v1.csv')

# 取 fund 列，计算日收益率
fund = df['fund']
daily_returns = fund.pct_change().dropna()

# ---------- 2. 计算日损益 ----------
daily_pnl = daily_returns * position

# ---------- 3. 历史法 VaR ----------
alpha = 1 - confidence_level
# 取损益分布的 alpha 分位数，VaR 报告为正的损失金额
var_quantile = np.percentile(daily_pnl, alpha * 100)
hist_var = -var_quantile   # 取负号 → 正数表示损失

# ---------- 4. 画日损益直方图 + VaR 线 ----------
fig, ax = plt.subplots(figsize=(10, 6))

n, bins, patches = ax.hist(daily_pnl, bins=50, edgecolor='black',
                           alpha=0.75, color='steelblue', label='日损益')

# VaR 竖线画在 alpha 分位数处（即 -hist_var）
ax.axvline(x=var_quantile, color='red', linestyle='--', linewidth=2.5,
           label=f'{confidence_level*100:.0f}% 1-day Historical VaR = {hist_var:,.2f} 元')

ax.set_xlabel('日损益（元）', fontsize=13)
ax.set_ylabel('频数', fontsize=13)
ax.set_title(f'日损益直方图  |  {confidence_level*100:.0f}% 一日历史 VaR', fontsize=14)
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()

# ---------- 5. 保存图片 ----------
figure_path = 'hist_var_histogram.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ---------- 6. 输出结果 ----------
result = {
    'hist_var_95_1d': hist_var,
    'figure_path': figure_path
}

print("=" * 50)
print(f"  置信水平:            {confidence_level*100:.0f}%")
print(f"  持有期:              1 天")
print(f"  头寸:                {position:,.0f} 元")
print(f"  样本数:              {len(daily_pnl)}")
print(f"  {confidence_level*100:.0f}% 一日历史 VaR:    {hist_var:,.2f} 元")
print("=" * 50)
