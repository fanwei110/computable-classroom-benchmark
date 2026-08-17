import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ============================================
# 参数设置
# ============================================
POSITION_VALUE = 1_000_000  # 头寸规模（人民币）
CONFIDENCE_LEVEL = 0.95     # 置信水平（可调参数）
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURES_DIR = 'figures'

# ============================================
# 1. 读取数据并构造日损益
# ============================================
# 读取CSV文件
df = pd.read_csv(DATA_PATH)

# 获取fund列日收益率
daily_returns = df['fund'].values

# 构造头寸日损益（人民币）
daily_pnl = POSITION_VALUE * daily_returns

# ============================================
# 2. 计算历史VaR（经验分布法）
# ============================================
# 将损益排序
sorted_pnl = np.sort(daily_pnl)

# 计算VaR对应的分位数索引
# 对于95%置信水平，VaR是第5百分位数
n = len(sorted_pnl)
var_index = int(np.floor(n * (1 - CONFIDENCE_LEVEL)))

# 确保索引有效
var_index = max(0, min(var_index, n - 1))

# 历史VaR（负值表示损失）
hist_var = sorted_pnl[var_index]

# 转换为正值表示损失金额
hist_var_loss = abs(hist_var)

# ============================================
# 3. 绘制直方图和VaR线
# ============================================
# 创建图形目录
Path(FIGURES_DIR).mkdir(parents=True, exist_ok=True)

# 设置绘图参数
plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['font.size'] = 12

fig, ax = plt.subplots(figsize=(12, 7))

# 绘制日损益直方图
n_bins = 50
n, bins, patches = ax.hist(daily_pnl, bins=n_bins, density=True, 
                           alpha=0.7, color='steelblue', 
                           edgecolor='white', linewidth=0.5,
                           label='日损益分布')

# 添加VaR竖线
ax.axvline(x=hist_var, color='darkred', linestyle='--', 
           linewidth=2.5, label=f'历史VaR ({CONFIDENCE_LEVEL*100:.0f}%置信)')

# 添加VaR标注
y_max = ax.get_ylim()[1]
ax.annotate(f'VaR = ¥{hist_var_loss:,.0f}\n({CONFIDENCE_LEVEL*100:.0f}% 置信水平)',
            xy=(hist_var, y_max * 0.85),
            xytext=(hist_var + np.std(daily_pnl) * 0.5, y_max * 0.9),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', 
                     edgecolor='darkred', alpha=0.9),
            arrowprops=dict(arrowstyle='->', color='darkred', 
                          connectionstyle='arc3,rad=-0.2'))

# 设置图形标签
ax.set_xlabel('日损益（人民币）', fontsize=14)
ax.set_ylabel('密度', fontsize=14)
ax.set_title(f'头寸日损益分布与历史VaR分析\n（头寸规模：¥{POSITION_VALUE:,} | 样本数：{n}天）', 
             fontsize=16, fontweight='bold')
ax.legend(loc='upper left', fontsize=12)
ax.grid(True, alpha=0.3, linestyle='--')

# 添加统计信息框
stats_text = f'均值：¥{np.mean(daily_pnl):,.0f}\n标准差：¥{np.std(daily_pnl):,.0f}\n'
stats_text += f'最小值：¥{np.min(daily_pnl):,.0f}\n最大值：¥{np.max(daily_pnl):,.0f}\n'
stats_text += f'VaR ({CONFIDENCE_LEVEL*100:.0f}%): ¥{hist_var_loss:,.0f}\n'
stats_text += f'样本数：{len(daily_pnl)}天'

ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()

# ============================================
# 4. 保存图形
# ============================================
figure_path = Path(FIGURES_DIR) / 'historical_var_analysis.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"图形已保存至: {figure_path}")

# ============================================
# 5. 填充结果字典
# ============================================
result = {
    'hist_var_95_1d': hist_var_loss,  # 95%一日历史VaR（人民币正值）
    'figure_path': str(figure_path)    # 图形文件路径
}

# 输出结果
print("\n" + "="*50)
print("VaR计算结果")
print("="*50)
print(f"置信水平：{CONFIDENCE_LEVEL*100}%")
print(f"头寸规模：¥{POSITION_VALUE:,}")
print(f"历史VaR（1日）：¥{hist_var_loss:,.2f}")
print(f"历史VaR（百分比）：{hist_var_loss/POSITION_VALUE*100:.4f}%")
print("="*50)

# 验证结果
print(f"\n结果字典: {result}")
