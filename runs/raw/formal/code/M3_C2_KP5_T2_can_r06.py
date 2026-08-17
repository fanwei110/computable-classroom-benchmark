import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数假设与设置 ====================
POSITION = 1_000_000              # 头寸规模（人民币）
CONFIDENCE_LEVEL = 0.95           # 置信水平（可调参数，例如改为 0.99 即可计算99%的VaR）
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'pnl_var_histogram.png'

# 设置 matplotlib 支持负号显示
plt.rcParams['axes.unicode_minus'] = False

# ==================== 1. 读取数据与构造日损益 ====================
# 读取课程数据快照
df = pd.read_csv(DATA_PATH)

# 提取 "fund" 列的日收益序列
# 假设：题目指明为"日收益序列"，即该列数据为日简单收益率，非价格序列，非对数收益率
daily_returns = df['fund']

# 构造头寸的日损益 (PnL = 头寸规模 * 日收益率)
daily_pnl = POSITION * daily_returns

# ==================== 2. 由经验分布计算历史 VaR ====================
# 计算显著性水平 (如 95% 置信水平对应 5% 的下侧分位数)
alpha = 1 - CONFIDENCE_LEVEL

# 使用经验分布计算损益的下侧分位数 (此值通常为负数，代表损失)
pnl_quantile = np.percentile(daily_pnl, alpha * 100)

# 在险价值 按惯例报告为正数，表示“处于风险中的价值”（潜在最大损失）
hist_var_rmb = -pnl_quantile

# ==================== 3. 画直方图并加带标注的 VaR 线 ====================
plt.figure(figsize=(10, 6))

# 绘制日损益分布直方图
plt.hist(daily_pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.7, density=False)

# 绘制带标注的 VaR 竖线 (位于损益分布的损失分位数处)
plt.axvline(x=pnl_quantile, color='red', linestyle='--', linewidth=2,
            label=f'{int(CONFIDENCE_LEVEL*100)}% 1-Day Historical VaR\n= {hist_var_rmb:,.2f} RMB')

# 添加图表元素
plt.title(f'Daily PnL Distribution & Historical VaR (Position: {POSITION:,.0f} RMB)')
plt.xlabel('Daily Profit and Loss (RMB)')
plt.ylabel('Frequency')
plt.legend(fontsize=11, loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# ==================== 4. 保存图形并填充 result ====================
# 保存图形
plt.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close()

# 严格遵循输出契约，构建结果字典
result = {
    'hist_var_95_1d': hist_var_rmb,
    'figure_path': FIGURE_PATH
}
