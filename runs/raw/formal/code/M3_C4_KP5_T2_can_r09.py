import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 1. 参数设置 ====================
position_value = 1_000_000       # 头寸金额（人民币元）
confidence_level = 0.95          # 置信水平（可调参数）
quantile_level = 1 - confidence_level  # 损益分布的左尾分位数

# ==================== 2. 读取数据与构造日损益 ====================
# 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 "fund" 列的日收益率序列
returns = df['fund']

# 构造头寸的日损益 (PnL)
pnl = returns * position_value

# ==================== 3. 计算历史 VaR ====================
# 按线性插值经验分位数（numpy 默认）计算分位数
# 95% VaR 对应损益分布的 5% 分位数
pnl_quantile = np.quantile(pnl, quantile_level)

# VaR 报告为正的损失金额
hist_var_95_1d = -pnl_quantile

# ==================== 4. 绘制直方图与 VaR 竖线 ====================
# 设置绘图风格
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, edgecolor='black', alpha=0.75, color='steelblue')

# 添加带标注的 VaR 竖线
plt.axvline(
    pnl_quantile, 
    color='red', 
    linestyle='dashed', 
    linewidth=2,
    label=f'{confidence_level*100:.0f}% 1-Day Hist VaR = ¥{hist_var_95_1d:,.2f}'
)

# 添加标注与图例
plt.title('Daily PnL Distribution and Historical Value at Risk (VaR)', fontsize=14)
plt.xlabel('Daily Profit and Loss (¥)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', alpha=0.3)

# ==================== 5. 保存图形并填充结果 ====================
fig_path = 'hist_var_plot.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# 严格按照输出契约存入字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': fig_path
}
