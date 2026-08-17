import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==========================================
# 参数设置 (可调)
# ==========================================
POSITION = 1_000_000          # 头寸：100万人民币
CONFIDENCE_LEVEL = 0.95       # 置信度：95%
FILE_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'hist_var_plot.png'

# ==========================================
# 1. 读取快照 CSV，构造头寸的日损益
# ==========================================
# 读取数据
df = pd.read_csv(FILE_PATH)

# 提取基金日收益率并剔除缺失值
returns = df['fund'].dropna()

# 构造日损益 (PnL)
pnl = POSITION * returns

# ==========================================
# 2. 由经验分布计算历史 VaR（人民币）
# ==========================================
# 计算损失分位数：alpha = 1 - 置信度
alpha = 1 - CONFIDENCE_LEVEL

# 计算 PnL 的左尾分位数 (通常为负数，代表损失)
pnl_percentile = np.percentile(pnl, alpha * 100)

# VaR 报告为正数，代表可能损失的最大额
hist_var_95_1d = -pnl_percentile

# ==========================================
# 3. 画直方图并加带标注的 VaR 线
# ==========================================
# 设置绘图样式
plt.style.use('seaborn-v0_8-darkgrid')
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制损益直方图
ax.hist(pnl, bins=50, color='steelblue', edgecolor='white', alpha=0.75)

# 添加 VaR 竖线 (画在原始 PnL 刻度上，即 pnl_percentile 的位置)
ax.axvline(x=pnl_percentile, color='red', linestyle='--', linewidth=2.5,
           label=f'{CONFIDENCE_LEVEL*100:.0f}% 1-Day VaR: {hist_var_95_1d:,.2f} RMB')

# 在图中做数值标注
# 获取y轴上限以确定文本位置
y_lim = ax.get_ylim()
ax.text(pnl_percentile, y_lim[1] * 0.9, 
        f'VaR = {hist_var_95_1d:,.2f} RMB\n(PnL = {pnl_percentile:,.2f})', 
        color='red', ha='right', va='top', fontsize=12, fontweight='bold',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='red', boxstyle='round,pad=0.5'))

# 设置标题与坐标轴
ax.set_title(f'Daily PnL Distribution & {CONFIDENCE_LEVEL*100:.0f}% 1-Day Historical VaR', fontsize=14, fontweight='bold')
ax.set_xlabel('Daily Profit and Loss (RMB)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.legend(fontsize=12, loc='upper left')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{x:,.0f}"))

plt.tight_layout()

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
fig.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close()

# 按照输出契约构造结果字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': FIGURE_PATH
}

# 课堂投屏展示结果
print(f"95% 1-day Historical VaR: {hist_var_95_1d:,.2f} RMB")
print(f"Figure saved to: {FIGURE_PATH}")
