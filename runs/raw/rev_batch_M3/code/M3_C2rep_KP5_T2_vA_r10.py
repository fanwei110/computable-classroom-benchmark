import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================
# 参数设定
# ==============================================
position = 1_000_000  # 头寸规模（人民币）
alpha = 0.95         # 置信水平（可调参数）

# ==============================================
# 1. 读取快照 CSV，构造头寸的日损益
# ==============================================
df = pd.read_csv('data/market_snapshot_v1.csv')
# 读取 'fund' 列的日收益序列，剔除可能的缺失值保证计算稳健
# 假设日收益率为小数形式（如0.01表示1%）
daily_returns = df['fund'].dropna()

# 构造头寸的日损益 (P&L)
pnl = position * daily_returns

# ==============================================
# 2. 由经验分布计算历史 VaR（人民币）
# ==============================================
# 历史 VaR 是损益分布的第 (1 - alpha) 分位数所对应的损失金额
# 对于 95% 置信水平，取 5% 分位数
var_percentile = 100 * (1 - alpha)
var_threshold = np.percentile(pnl, var_percentile)

# 将损失表示为正数（若分位数为负，取正代表亏损；若为正，代表最差情况仍盈利，VaR为负）
hist_var_95_1d = -var_threshold

# ==============================================
# 3. 画直方图并加带标注的 VaR 线
# ==============================================
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.75)

# 绘制带标注的 VaR 竖线
plt.axvline(x=var_threshold, color='red', linestyle='--', linewidth=2,
            label=f'{alpha*100:.0f}% 1-Day VaR: {hist_var_95_1d:,.2f} RMB')

plt.title('Daily P&L Distribution and Historical VaR', fontsize=14)
plt.xlabel('Daily P&L (RMB)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.5)

# ==============================================
# 4. 保存图形并填充 result
# ==============================================
figure_path = 'var_pnl_histogram.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 严格遵循输出契约
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}
