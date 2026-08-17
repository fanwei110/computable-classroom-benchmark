import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 假设与参数设置 ====================
POSITION = 1_000_000          # 头寸（人民币）
CONFIDENCE_LEVEL = 0.95       # 置信水平（参数化，可调）
FIGURE_PATH = 'var_histogram.png'  # 图形保存路径

# ==================== 1. 读取数据与构造损益 ====================
# 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 'fund' 列的日收益率序列，并剔除可能的缺失值
# 假设：日收益率以小数形式表示（如 0.01 代表 1%）
returns = df['fund'].dropna().values

# 构造头寸的日损益（P&L = 头寸规模 × 日收益率）
daily_pnl = POSITION * returns

# ==================== 2. 计算历史 VaR ====================
# 置信水平为 95%，则显著性水平 (左尾概率) 为 5%
alpha = 1 - CONFIDENCE_LEVEL

# 使用经验分布计算分位数（历史模拟法）
# np.percentile 默认使用线性插值，这在历史VaR计算中是标准且可复现的做法
pnl_var_quantile = np.percentile(daily_pnl, 100 * alpha)

# VaR 惯例上报告为正数（表示可能发生的损失规模）
# 如果分位数本身是正数（极端牛市情况），VaR理论值为负，但仍遵从数学计算取负
hist_var_95_1d = -pnl_var_quantile

# ==================== 3. 画直方图并加带标注的 VaR 线 ====================
# 为保证课堂投屏兼容性（避免中文字体缺失导致乱码），图表文字采用英文
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制日损益分布直方图
ax.hist(daily_pnl, bins=50, color='steelblue', edgecolor='white', alpha=0.8)

# 绘制 VaR 竖线（在 P&L 坐标系下，位置即为 pnl_var_quantile）
ax.axvline(x=pnl_var_quantile, color='red', linestyle='--', linewidth=2)

# 添加带标注的文本（为了美观，将文本放置在线的左侧稍高处）
# 获取y轴上限以定位文本
ylim_top = ax.get_ylim()[1]
ax.text(pnl_var_quantile, ylim_top * 0.9, 
        f'{CONFIDENCE_LEVEL*100:.0f}% 1-Day Hist VaR\n= {hist_var_95_1d:,.2f} RMB', 
        color='red', ha='right', va='top', fontsize=12, fontweight='bold',
        bbox=dict(facestyle='round,pad=0.3', edgecolor='red', alpha=0.2))

# 设置图表标签与标题
ax.set_title(f'Daily P&L Distribution for {POSITION/1e6:.1f}M RMB Position', fontsize=14)
ax.set_xlabel('Daily Profit and Loss (RMB)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.grid(True, linestyle=':', alpha=0.6)

# ==================== 4. 保存图形并填充 result ====================
# 保存图形
fig.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close(fig)  # 释放内存

# 将结果存入字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': FIGURE_PATH
}
