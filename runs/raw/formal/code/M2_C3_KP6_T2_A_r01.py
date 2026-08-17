import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 读取数据
df = pd.read_excel('data.xlsx', sheet_name='fund')
df['日期'] = pd.to_datetime(df['日期'])
df = df.sort_values('日期').reset_index(drop=True)

# 无风险利率
rf = 0.021  # 2.1%

# 窗口参数（可调整）
window = 60  # 60个交易日

# 计算日收益率
df['daily_return'] = df['fund'].pct_change()

# 计算滚动年化夏普比率
rolling_mean = df['daily_return'].rolling(window=window).mean()  # 日平均收益率
rolling_std = df['daily_return'].rolling(window=window).std(ddof=1)  # 日波动率

# 年化：均值和标准差都乘以sqrt(252)
annualized_return = rolling_mean * 252  # 年化收益率
annualized_std = rolling_std * np.sqrt(252)  # 年化波动率

# 年化夏普比率
df['rolling_sharpe'] = (annualized_return - rf) / annualized_std

# 最后一个窗口的数值
rolling_sharpe_last = df['rolling_sharpe'].iloc[-1]

print(f"最后一个窗口的60日滚动年化夏普比率: {rolling_sharpe_last:.6f}")

# 绘制曲线
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(df['日期'], df['rolling_sharpe'], linewidth=1.5, color='#1f77b4')
ax.axhline(y=0, color='red', linestyle='--', linewidth=0.8, alpha=0.7)
ax.axhline(y=rf, color='green', linestyle='--', linewidth=0.8, alpha=0.7, label=f'rf={rf*100}%')

# 标注最后一个值
last_date = df['日期'].iloc[-1]
ax.scatter(last_date, rolling_sharpe_last, color='red', s=100, zorder=5)
ax.annotate(f'{rolling_sharpe_last:.4f}', 
            xy=(last_date, rolling_sharpe_last),
            xytext=(last_date - pd.Timedelta(days=60), rolling_sharpe_last + 0.1),
            fontsize=12, fontweight='bold', color='red',
            arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

ax.set_xlabel('日期', fontsize=12)
ax.set_ylabel('滚动年化夏普比率', fontsize=12)
ax.set_title(f'60日滚动年化夏普比率 (rf={rf*100}%)', fontsize=14, fontweight='bold')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()

# 保存图表
figure_path = 'rolling_sharpe_ratio.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.show()

print(f"\n图表已保存至: {figure_path}")

# 存入结果字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': os.path.abspath(figure_path)
}

print(f"\n结果字典:")
print(f"  rolling_sharpe_last: {result['rolling_sharpe_last']:.6f}")
print(f"  figure_path: {result['figure_path']}")
