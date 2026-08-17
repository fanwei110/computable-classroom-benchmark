import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 参数设置 (可调)
# ==========================================
position = 1_000_000         # 头寸 (人民币元)
confidence_level = 0.95      # 置信水平 (可调参数)
alpha = 1 - confidence_level # 显著性水平

# ==========================================
# 1. 读取快照 CSV，构造头寸的日损益
# ==========================================
# 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取日收益序列并构造日损益 (PnL)
# 假设 'fund' 列为日收益率 (如0.01表示1%)
daily_returns = df['fund']
pnl = daily_returns * position

# ==========================================
# 2. 由经验分布计算历史 VaR（人民币）
# ==========================================
# 计算 alpha 分位数 (即左尾 5% 分位数)
var_percentile_value = np.percentile(pnl, 100 * alpha)

# 在险价值 通常以正数表示损失，因此取负值
hist_var_95_1d = -var_percentile_value

# ==========================================
# 3. 画直方图并加带标注的 VaR 线
# ==========================================
# 设置绘图风格
plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制日损益直方图
ax.hist(pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.75)

# 绘制 VaR 竖线 (在 PnL 轴上，VaR 对应的是负的损失额，即 var_percentile_value)
ax.axvline(var_percentile_value, color='red', linestyle='--', linewidth=2, 
           label=f'{confidence_level*100:.0f}% 1-Day Historical VaR\n= {hist_var_95_1d:,.2f} RMB')

# 添加标注与排版
ax.set_title(f'Daily PnL Distribution & Historical VaR (Confidence: {confidence_level*100:.0f}%)', fontsize=14)
ax.set_xlabel('Daily Profit and Loss (RMB)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.legend(fontsize=11)

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
figure_path = 'hist_var_plot.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# 封装结果
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}
