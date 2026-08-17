import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. 构造/读取课程数据快照
# ==========================================
# 由于未提供外部数据文件，为满足“不留占位值、输出确定可复现”的要求，
# 此处使用固定随机种子生成一段模拟的“fund”基金日收益率序列。
# 在实际业务中，此段可替换为: df = pd.read_csv('your_data.csv')
np.random.seed(42)  # 固定种子确保结果可复现
num_days = 1000
simulated_returns = np.random.normal(loc=0.0005, scale=0.015, size=num_days)
df = pd.DataFrame({'fund': simulated_returns})

# ==========================================
# 2. 参数设定与损益计算
# ==========================================
# 初始头寸 (人民币)
position_size = 1_000_000  

# 置信水平 (可调参数)
confidence_level = 0.95   

# 计算日损益序列 (人民币)
daily_pnl = position_size * df['fund']

# ==========================================
# 3. 计算 95% 一日历史 VaR
# ==========================================
# 历史模拟法 VaR 是损益分布的左尾分位数
alpha = 1 - confidence_level
pnl_var_percentile = np.percentile(daily_pnl, alpha * 100)

# 金融惯例中 VaR 以正数报告最大可能损失
hist_var_95_1d_rmb = abs(pnl_var_percentile)

# ==========================================
# 4. 绘制直方图与标注
# ==========================================
plt.figure(figsize=(10, 6))

# 绘制日损益分布直方图
plt.hist(daily_pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.75)

# 绘制 95% VaR 竖线 (对应在损益坐标轴上的实际分位点)
plt.axvline(pnl_var_percentile, color='red', linestyle='--', linewidth=2, 
            label=f'{confidence_level*100:.0f}% 1-Day VaR Line')

# 增加带箭头的文本标注
y_lim_max = plt.ylim()[1]
plt.annotate(f'95% 1-Day VaR\n= {hist_var_95_1d_rmb:,.2f} RMB',
             xy=(pnl_var_percentile, y_lim_max * 0.4),    # 箭头指向点
             xytext=(pnl_var_percentile * 0.4, y_lim_max * 0.8),  # 文本位置
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=12,
             color='red',
             fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="red", alpha=0.8))

# 设置图表标签和标题
plt.title('Distribution of Daily PnL & 95% 1-Day Historical VaR', fontsize=14)
plt.xlabel('Daily PnL (RMB)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper right')

# 保存图像
figure_path = 'daily_pnl_var_histogram.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 5. 封装输出契约
# ==========================================
result = {
    'hist_var_95_1d': hist_var_95_1d_rmb,
    'figure_path': figure_path
}
