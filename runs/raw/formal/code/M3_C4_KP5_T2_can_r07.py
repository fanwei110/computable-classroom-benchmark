import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 参数设置
# ==========================================
POSITION = 1_000_000              # 头寸金额（人民币）
CONFIDENCE_LEVEL = 0.95           # 置信水平（可调参数）
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'pnl_var_distribution.png'

# ==========================================
# 1. 读取快照 CSV，构造头寸的日损益
# ==========================================
df = pd.read_csv(DATA_PATH)
daily_returns = df['fund'].dropna().values
daily_pnl = POSITION * daily_returns  # 构造日损益分布

# ==========================================
# 2. 按线性插值经验分位数计算历史 VaR
# ==========================================
# VaR 对应损益分布的左尾分位数 (1 - 置信水平)
alpha = 1 - CONFIDENCE_LEVEL

# numpy 的 quantile 默认使用线性插值 (method='linear')，符合课程计算约定
quantile_pnl = np.quantile(daily_pnl, alpha)

# VaR 报告为正的损失金额
hist_var = -quantile_pnl

# ==========================================
# 3. 画直方图并加带标注的 VaR 线
# ==========================================
plt.figure(figsize=(10, 6))
plt.hist(daily_pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.7)

# 画出 VaR 竖线 (在 PnL 轴上的实际位置为 -hist_var)
var_x = -hist_var
plt.axvline(x=var_x, color='red', linestyle='--', linewidth=2)

# 在线上添加文本标注
# 根据直方图高度动态调整标注位置，避免遮挡
ymax = plt.ylim()[1]
plt.text(var_x, ymax * 0.9, 
         f'{CONFIDENCE_LEVEL*100:.0f}% 1-Day Hist VaR\n{hist_var:,.2f} RMB', 
         color='red', ha='right', va='top', fontsize=11,
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='red', boxstyle='round,pad=0.5'))

plt.title(f'Daily P&L Distribution and {CONFIDENCE_LEVEL*100:.0f}% Historical VaR', fontsize=14)
plt.xlabel('Daily P&L (RMB)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.5)

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
plt.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close()

result = {
    'hist_var_95_1d': hist_var,
    'figure_path': FIGURE_PATH
}
