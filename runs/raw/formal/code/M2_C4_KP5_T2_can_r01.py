import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# 可调参数
# ------------------------------
CONFIDENCE_LEVEL = 0.95          # 置信水平
POSITION_VALUE = 1_000_000.0     # 头寸本金（人民币）
DATA_PATH = "data/market_snapshot_v1.csv"
FIGURE_PATH = "var_hist_plot.png"

# ------------------------------
# 1. 读取数据并计算日损益
# ------------------------------
# 假定 CSV 中包含 "fund" 列，为小数形式的日收益率
df = pd.read_csv(DATA_PATH)
returns = df["fund"].dropna()   # 日收益序列

# 日损益 = 头寸价值 × 日收益率
profit_loss = POSITION_VALUE * returns.values

# ------------------------------
# 2. 计算历史 VaR（线性插值经验分位数）
# ------------------------------
alpha = 1.0 - CONFIDENCE_LEVEL
percentile_point = np.percentile(profit_loss, alpha * 100)   # 损益分位点（通常为负）
var_loss = -percentile_point          # 报告为正的损失金额

# ------------------------------
# 3. 画图并标注 VaR 线
# ------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(profit_loss, bins=50, alpha=0.7, color='steelblue', edgecolor='white',
        label='Daily P&L distribution')
ax.axvline(percentile_point, color='red', linestyle='dashed', linewidth=2,
           label=f'Historical VaR {CONFIDENCE_LEVEL*100:.0f}%')
# 添加文字标注（显示损失金额）
ax.annotate(f'VaR = ¥{var_loss:,.2f}\n(P&L = {percentile_point:,.2f})',
            xy=(percentile_point, ax.get_ylim()[1]*0.8),
            xytext=(percentile_point + (profit_loss.max()-profit_loss.min())*0.1,
                    ax.get_ylim()[1]*0.8),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=10, color='red', fontweight='bold')
ax.set_xlabel('Profit / Loss (RMB)')
ax.set_ylabel('Frequency')
ax.set_title(f'Daily P&L Distribution & {CONFIDENCE_LEVEL*100:.0f}% Historical VaR')
ax.legend()
plt.tight_layout()
fig.savefig(FIGURE_PATH, dpi=150)
plt.close(fig)

# ------------------------------
# 4. 输出结果
# ------------------------------
result = {
    'hist_var_95_1d': var_loss,
    'figure_path': FIGURE_PATH
}

# 打印以供课堂投屏验证
print(result)
