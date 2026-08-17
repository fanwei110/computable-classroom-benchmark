import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------------- 可调参数 -------------------------
CONFIDENCE_LEVEL = 0.95          # 置信水平，可更改为 0.99 等
POSITION_VALUE = 1_000_000.0    # 头寸金额（人民币）
DATA_PATH = 'data/market_snapshot_v1.csv'  # 数据文件路径
FIGURE_FILENAME = 'var_histogram.png'      # 输出图形文件名
# -----------------------------------------------------------

# 1. 读取 CSV，构造头寸的日损益
df = pd.read_csv(DATA_PATH)
# 假设 "fund" 列为小数形式的日收益率（例如 0.01 代表 1%）
returns = df['fund'].dropna().astype(float)
pnl = POSITION_VALUE * returns          # 日损益 = 头寸 × 收益率

# 2. 由经验分布计算历史 VaR（人民币）
#    VaR 通常定义为损益分布左尾的分位数对应的损失（正数）。
#    对于多头头寸，在 (1 - conf) 分位数的损益为负值时，VaR = -该分位数。
var_percentile = (1 - CONFIDENCE_LEVEL) * 100
pnl_quantile = np.percentile(pnl, var_percentile)   # 损益的分位数（一般为负）
hist_var_95_1d = -pnl_quantile                      # 转为正数的损失金额

# 3. 画直方图并标注 VaR 线
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制日损益直方图
n, bins, patches = ax.hist(pnl, bins='auto', density=True,
                           alpha=0.7, color='steelblue', edgecolor='white',
                           label='Daily P&L distribution')

# 画 VaR 竖线（注意：在损益的分位数处画线，该值通常为负数）
ax.axvline(x=pnl_quantile, color='red', linestyle='--', linewidth=2,
           label=f'{CONFIDENCE_LEVEL*100:.0f}% 1-Day Historical VaR\n'
                 f'({hist_var_95_1d:,.2f} CNY)')

# 标注文字（为避免重叠，自动放置）
ymin, ymax = ax.get_ylim()
ax.annotate(f'VaR = {hist_var_95_1d:,.2f} CNY',
            xy=(pnl_quantile, ymax * 0.9),
            xytext=(pnl_quantile - (pnl.max() - pnl.min()) * 0.2, ymax * 0.85),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
            fontsize=11, color='red', ha='center')

ax.set_xlabel('Profit / Loss (CNY)')
ax.set_ylabel('Density')
ax.set_title(f'Daily P&L Distribution and {CONFIDENCE_LEVEL*100:.0f}% Historical VaR\n'
             f'Position: {POSITION_VALUE:,.0f} CNY')
ax.legend()
plt.tight_layout()

# 4. 保存图形
fig_path = os.path.abspath(FIGURE_FILENAME)
plt.savefig(fig_path, dpi=150)
plt.close()

# ------------------------- 输出结果 -------------------------
result = {
    'hist_var_95_1d': round(hist_var_95_1d, 2),
    'figure_path': fig_path
}

# 便于教师查看，打印 result
print("=== 计算结果 ===")
print(f"95% 1-Day Historical VaR (CNY): {result['hist_var_95_1d']:,.2f}")
print(f"图形已保存至: {result['figure_path']}")
