import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# ==================== 参数设置 ====================
CONFIDENCE_LEVEL = 0.95  # 可调置信水平
POSITION_VALUE = 1_000_000  # 头寸规模（元）
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'var_histogram.png'

# ==================== 1. 读取数据并构造日损益 ====================
# 读取CSV文件
df = pd.read_csv(DATA_PATH)

# 提取fund列的日收益率序列
returns = df['fund'].values

# 构造头寸的日损益（元）：损益 = 头寸价值 × 收益率
daily_pnl = POSITION_VALUE * returns

# ==================== 2. 计算历史VaR ====================
# 使用numpy默认的线性插值经验分位数
# 损失分位数对应 (1 - 置信水平) 的下尾
loss_quantile = 1 - CONFIDENCE_LEVEL

# np.percentile 默认使用线性插值
# 小分位数对应的损益（负值表示损失）
var_pnl = np.percentile(daily_pnl, loss_quantile * 100)

# VaR报告为正的损失金额
hist_var_95_1d = -var_pnl

# ==================== 3. 绘制直方图并标注VaR ====================
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制损益分布直方图
n, bins, patches = ax.hist(daily_pnl, bins=50, edgecolor='black', 
                           alpha=0.7, color='steelblue', density=True)

# 添加VaR竖线标注
ax.axvline(x=var_pnl, color='red', linewidth=2.5, linestyle='--',
           label=f'{int(CONFIDENCE_LEVEL*100)}% 历史VaR: ¥{hist_var_95_1d:,.0f}')

# 添加标注文本
ymin, ymax = ax.get_ylim()
ax.annotate(f'VaR = ¥{hist_var_95_1d:,.0f}\n(损失分位数)',
            xy=(var_pnl, ymax * 0.85),
            xytext=(var_pnl - (bins[-1] - bins[0]) * 0.25, ymax * 0.9),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=11, color='red', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.8))

# 设置图形属性
ax.set_xlabel('日损益（人民币）', fontsize=12)
ax.set_ylabel('频率密度', fontsize=12)
ax.set_title(f'头寸价值 ¥{POSITION_VALUE:,} 的日损益分布\n'
             f'{int(CONFIDENCE_LEVEL*100)}% 历史VaR（{len(returns)}个交易日样本）',
             fontsize=13, fontweight='bold')
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3)

# 设置x轴范围以包含大部分数据
x_min = np.percentile(daily_pnl, 0.1)
x_max = np.percentile(daily_pnl, 99.9)
ax.set_xlim(x_min, x_max)

plt.tight_layout()
plt.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 4. 填充结果字典 ====================
result = {
    'hist_var_95_1d': float(hist_var_95_1d),
    'figure_path': os.path.abspath(FIGURE_PATH)
}

# ==================== 输出确认 ====================
print(f"头寸规模: ¥{POSITION_VALUE:,}")
print(f"置信水平: {CONFIDENCE_LEVEL*100}%")
print(f"95% 1日历史VaR: ¥{hist_var_95_1d:,.2f}")
print(f"图形保存路径: {result['figure_path']}")
print(f"\n结果字典: {result}")
