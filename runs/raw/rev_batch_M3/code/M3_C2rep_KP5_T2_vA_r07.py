import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 假设与参数设置 ====================
# 头寸金额（人民币）
POSITION = 1_000_000

# 置信水平（可调参数）
CONFIDENCE_LEVEL = 0.95

# 数据路径
DATA_PATH = 'data/market_snapshot_v1.csv'

# 图像保存路径
FIGURE_PATH = 'var_pnl_histogram.png'

# ==================== 1. 读取快照 CSV，构造头寸的日损益 ====================
# 读取数据
df = pd.read_csv(DATA_PATH)

# 提取 fund 列的日收益率序列
# 假设：fund 列记录的是日收益率（小数形式，如 0.01 表示 1%）
daily_returns = df['fund']

# 计算日损益 (PnL)，单位：人民币
# 损益 = 头寸金额 * 日收益率
pnl = POSITION * daily_returns

# ==================== 2. 由经验分布计算 95% 历史 VaR（人民币） ====================
# 历史模拟法：VaR 是损益分布左侧 (1 - 置信水平) 分位数的绝对值
# 首先计算 PnL 的 alpha 分位数 (alpha = 1 - confidence_level)
alpha = 1 - CONFIDENCE_LEVEL
pnl_quantile = np.quantile(pnl, alpha)

# VaR 报告为正数（表示预期的最大损失金额）
hist_var = -pnl_quantile

# ==================== 3. 画直方图并加带标注的 VaR 线 ====================
# 设置绘图风格
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制日损益分布直方图
ax.hist(pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.7)

# 绘制 VaR 竖线
ax.axvline(x=pnl_quantile, color='red', linestyle='--', linewidth=2,
           label=f'{CONFIDENCE_LEVEL*100:.0f}% 1-Day VaR\n'
                 f'({hist_var:,.2f} RMB)')

# 添加标注与标题
ax.set_title('Daily PnL Distribution and Historical VaR', fontsize=14)
ax.set_xlabel('Daily Profit and Loss (RMB)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.legend(fontsize=11, loc='upper right')

# ==================== 4. 保存图形并填充 result ====================
# 保存图形
plt.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close()

# 填充结果字典
result = {
    'hist_var_95_1d': hist_var,
    'figure_path': FIGURE_PATH
}

# 打印结果以便课堂展示
print(f"95% 1-Day Historical VaR: {result['hist_var_95_1d']:,.2f} RMB")
print(f"Figure saved to: {result['figure_path']}")
