import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 参数设置
# ==========================================
file_path = 'data/market_snapshot_v1.csv'
position_size = 1_000_000  # 头寸（人民币元）
confidence_level = 0.95    # 置信水平（可调参数）
figure_path = 'var_pnl_distribution.png'

# ==========================================
# 步骤1：读取快照 CSV，构造头寸的日损益
# ==========================================
# 读取数据
df = pd.read_csv(file_path)

# 提取日收益序列并去除可能的缺失值
daily_returns = df['fund'].dropna()

# 计算日损益 (P&L)
daily_pnl = position_size * daily_returns

# ==========================================
# 步骤2：由经验分布计算历史 VaR（人民币）
# ==========================================
# 计算左尾分位数对应的概率
alpha = 1 - confidence_level

# 计算损益分布的分位数 (例如95%置信水平对应5%分位数)
pnl_quantile = np.quantile(daily_pnl, alpha)

# VaR定义为损失额，取正值报告
hist_var_95_1d = -pnl_quantile

# ==========================================
# 步骤3：画直方图并加带标注的 VaR 线
# ==========================================
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制日损益分布直方图
ax.hist(daily_pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.75, label='Daily P&L Distribution')

# 绘制 VaR 竖线 (即损益分布的损失分位数线)
ax.axvline(pnl_quantile, color='red', linestyle='dashed', linewidth=2, label=f'{confidence_level*100:.0f}% VaR Line')

# 为竖线添加标注
# 获取当前y轴上限以合理放置文字
ylim_max = ax.get_ylim()[1]
text_x_position = pnl_quantile - (daily_pnl.max() - daily_pnl.min()) * 0.05  # 稍微偏左放置文字，防止遮挡线条
ax.text(text_x_position, ylim_max * 0.85, 
        f'{confidence_level*100:.0f}% 1-day Hist VaR\n¥{hist_var_95_1d:,.2f}',
        color='red', fontsize=12, fontweight='bold',
        ha='right', va='top',
        bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='red', alpha=0.8))

# 设置图表标题和坐标轴标签
ax.set_title(f'Daily P&L Distribution and {confidence_level*100:.0f}% Historical VaR (Position: ¥{position_size:,})', fontsize=14)
ax.set_xlabel('Daily Profit & Loss (RMB)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.legend(fontsize=11)

# ==========================================
# 步骤4：保存图形并填充 result
# ==========================================
# 保存图形
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# 填充结果字典，确保返回标准 Python float
result = {
    'hist_var_95_1d': float(hist_var_95_1d),
    'figure_path': figure_path
}
