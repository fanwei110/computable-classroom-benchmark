import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 参数设置 (置信水平参数化，方便调整)
# ==========================================
confidence_level = 0.95          # 置信水平
position = 1_000_000           # 头寸规模：100万元
data_file = 'data/market_snapshot_v1.csv'
figure_path = 'hist_var_plot.png'

# 设置中文字体和负号显示，防止课堂投屏乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 步骤1：读取快照 CSV，构造头寸的日损益
# ==========================================
# 读取数据
df = pd.read_csv(data_file)

# 假设 fund 列为基金净值，计算日收益率
daily_returns = df['fund'].pct_change().dropna()

# 构造头寸的日损益（人民币）
pnl = position * daily_returns

# ==========================================
# 步骤2：由经验分布计算历史 VaR（人民币）
# ==========================================
alpha = 1 - confidence_level
# 历史 VaR 取损益分布的左分位数，取负号以正数表示潜在损失金额
hist_var_95_1d = -np.percentile(pnl, alpha * 100)

# ==========================================
# 步骤3：画直方图并加带标注的 VaR 线
# ==========================================
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制日损益直方图
ax.hist(pnl, bins=50, color='skyblue', edgecolor='black', alpha=0.7)

# 绘制 VaR 线 (对应在 PnL 上的左分位数位置，即 -VaR)
var_line_x = -hist_var_95_1d
ax.axvline(x=var_line_x, color='red', linestyle='--', linewidth=2,
           label=f'{confidence_level*100:.0f}% 1-Day VaR = {hist_var_95_1d:,.2f} RMB')

# 添加标注与图表装饰
ax.set_title(f'日损益分布直方图及历史在险价值
ax.set_xlabel('日损益金额 (人民币)')
ax.set_ylabel('频数')
ax.legend(loc='upper right')
ax.grid(True, linestyle='--', alpha=0.5)

# ==========================================
# 步骤4：保存图形并填充 result
# ==========================================
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# 将结果存入字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}

# 输出 VaR 数值
print(f"在 {confidence_level*100:.0f}% 置信水平下，1日历史VaR为：{hist_var_95_1d:,.2f} 元人民币")
