import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 计算日收益率
df['returns'] = df['fund'].pct_change().dropna()

# 剔除缺失值
returns = df['returns'].dropna()

# 设置头寸和置信水平
position = 1_000_000  # 100万元
confidence_level = 0.95  # 可调参数

# 计算历史法VaR
var_percentile = np.percentile(returns, (1 - confidence_level) * 100)
hist_var_95_1d = position * var_percentile

print(f"历史法VaR (95%置信水平, 1天): {hist_var_95_1d:.2f} 元")
print(f"收益率分位数 ({((1-confidence_level)*100):.1f}%): {var_percentile:.6f}")

# 计算日损益
daily_pnl = returns * position

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制日损益直方图
n, bins, patches = ax.hist(daily_pnl, bins=50, edgecolor='black', alpha=0.7, 
                            color='steelblue', label='日损益分布')

# 标注VaR线
ax.axvline(x=hist_var_95_1d, color='red', linestyle='--', linewidth=2, 
           label=f'历史法VaR (95%): {hist_var_95_1d:,.2f} 元')

# 设置图表样式
ax.set_xlabel('日损益 (元)', fontsize=12)
ax.set_ylabel('频数', fontsize=12)
ax.set_title(f'历史法VaR分析 - 日损益分布\n置信水平: {confidence_level*100}%', fontsize=14)
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# 添加文本说明
textstr = f'头寸: ¥{position:,.0f}\nVaR值: ¥{hist_var_95_1d:,.2f}\n置信水平: {confidence_level*100}%'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.tight_layout()

# 保存图表
os.makedirs('result', exist_ok=True)
figure_path = 'result/historical_var_distribution.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.show()

# 构建结果字典
result = {
    'hist_var_95_1d': hist_var_95_1d,
    'figure_path': figure_path
}

print(f"\n结果字典:")
print(f"hist_var_95_1d: {result['hist_var_95_1d']:.2f}")
print(f"figure_path: {result['figure_path']}")

# 验证结果
print(f"\n数据验证:")
print(f"收益率数据点数: {len(returns)}")
print(f"日损益均值: {daily_pnl.mean():.2f} 元")
print(f"日损益标准差: {daily_pnl.std():.2f} 元")
print(f"最小日损益: {daily_pnl.min():.2f} 元")
print(f"最大日损益: {daily_pnl.max():.2f} 元")
