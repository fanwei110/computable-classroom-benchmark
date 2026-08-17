import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------- 可调参数 ----------
CONFIDENCE = 0.95                # 置信水平
ALPHA = 1 - CONFIDENCE           # 显著性水平（损失分位数）
POSITION = 1_000_000             # 头寸金额（人民币）
# ------------------------------

# 1. 读取数据，构造日损益
df = pd.read_csv('data/market_snapshot_v1.csv')
returns = df['fund'].values                     # 日收益序列

# 若收益率呈现百分比形式（如 -2.5 表示 -2.5%），转换为小数
if np.max(np.abs(returns)) > 1:
    returns = returns / 100.0

pnl = POSITION * returns                        # 每日损益（人民币）

# 2. 经验分布计算历史 VaR
var_percentile = np.percentile(pnl, 100 * ALPHA)  # 损益分布的左尾分位数
hist_var_95_1d = -var_percentile                  # VaR 定义为正数（损失金额）

# 3. 绘制直方图并标注 VaR
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(pnl, bins=50, edgecolor='black', alpha=0.7, color='skyblue',
        label='Daily PnL')
ax.axvline(x=var_percentile, color='red', linestyle='--', linewidth=2,
           label=f'Historical VaR ({CONFIDENCE*100:.0f}%): ¥{hist_var_95_1d:,.2f}')
ax.set_xlabel('Daily PnL (¥)')
ax.set_ylabel('Frequency')
ax.set_title(f'Distribution of Daily PnL with {CONFIDENCE*100:.0f}% Historical VaR')
ax.legend()

# 保存图形
figure_path = 'var_hist.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 4. 输出要求的字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}
