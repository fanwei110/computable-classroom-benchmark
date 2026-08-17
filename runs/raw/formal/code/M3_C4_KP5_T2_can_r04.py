import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==================== 参数设置 ====================
position = 1_000_000          # 头寸金额（人民币）
confidence_level = 0.95       # 置信水平（可调参数）
data_path = 'data/market_snapshot_v1.csv'
figure_path = 'pnl_histogram_with_var.png'

# ==================== 1. 读取数据与构造日损益 ====================
# 读取CSV数据
df = pd.read_csv(data_path)

# 提取日收益率序列（小数表示）
returns = df['fund'].values

# 构造日损益（人民币金额）
pnl = returns * position

# ==================== 2. 计算95%一日历史VaR ====================
# 损失分位数：取损益分布的 (1 - 置信水平) 分位数
# 使用 numpy 默认的线性插值法 (method='linear')
alpha = 1 - confidence_level
var_value = np.quantile(pnl, alpha)

# VaR 报告为正的损失金额
hist_var_95_1d = -var_value

# ==================== 3. 画直方图并加带标注的VaR线 ====================
# 设置matplotlib支持中文显示与负号
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

# 绘制损益分布直方图
ax.hist(pnl, bins=50, color='steelblue', edgecolor='white', alpha=0.75)

# 添加VaR竖线 (损失为正，对应PnL的负值处)
ax.axvline(var_value, color='red', linestyle='--', linewidth=2, 
           label=f'{confidence_level:.0%} 1-Day Historical VaR')

# 添加标注
ax.annotate(f'VaR = ¥{hist_var_95_1d:,.2f}',
            xy=(var_value, 0), xytext=(var_value - position*0.02, ax.get_ylim()[1] * 0.8),
            arrowprops=dict(facecolor='red', shrink=0.05, width=1.5, headwidth=8),
            fontsize=12, color='red', fontweight='bold')

ax.set_title('Daily PnL Distribution and Historical VaR', fontsize=14)
ax.set_xlabel('Daily PnL (¥)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.legend(fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# ==================== 4. 保存图形与输出结果 ====================
# 保存图形
fig.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close(fig)

# 构造输出契约字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}
