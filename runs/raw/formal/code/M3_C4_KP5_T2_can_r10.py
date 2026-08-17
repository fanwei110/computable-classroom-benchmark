import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 参数设置
# ==========================================
position = 1_000_000          # 头寸金额（元）
confidence_level = 0.95       # 置信水平（可调参数）
alpha = 1 - confidence_level # 显著性水平（左尾分位数）

# ==========================================
# 1. 读取快照 CSV，构造头寸的日损益
# ==========================================
df = pd.read_csv('data/market_snapshot_v1.csv')
returns = df['fund'].dropna()  # 日收益率序列（小数表示）
pnl = returns * position      # 日损益金额（人民币元）

# ==========================================
# 2. 按线性插值经验分位数（numpy 默认）计算 95% 历史 VaR
# ==========================================
# numpy.quantile 默认使用 linear 插值方法
pnl_quantile = np.quantile(pnl, alpha)  
# VaR 报告为正的损失金额，即取相反数
hist_var_95_1d = -pnl_quantile  

# ==========================================
# 3. 画直方图并加带标注的 VaR 线
# ==========================================
plt.figure(figsize=(10, 6))
plt.hist(pnl, bins=50, color='steelblue', edgecolor='black', alpha=0.75)

# 添加 VaR 竖线，x 坐标为损益的分位点值
plt.axvline(x=pnl_quantile, color='red', linestyle='--', linewidth=2,
            label=f'{confidence_level:.0%} 1-Day Historical VaR\n= {hist_var_95_1d:,.2f} RMB')

plt.title('Daily PnL Distribution and Historical VaR', fontsize=14)
plt.xlabel('Daily PnL (RMB)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.legend(fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# ==========================================
# 4. 保存图形并填充 result 字典
# ==========================================
figure_path = 'hist_var_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 按输出契约存入字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}
