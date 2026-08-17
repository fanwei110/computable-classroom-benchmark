import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

# ============================================================
# 1. 读取数据
# ============================================================
data_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(data_path)

# 检查必要列是否存在，假设数据有 'date' 和 'fund' 列
# 如果日期列存在，设置索引；否则使用整数索引
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

# 提取基金收益序列
fund_returns = df['fund'].dropna()

# ============================================================
# 2. 参数设定
# ============================================================
risk_free_rate_annual = 0.021  # 年化无风险利率 2.1%
window = 60  # 滚动窗口（可调参数）

# 将年化无风险利率转换为日度（假设252个交易日）
risk_free_rate_daily = risk_free_rate_annual / 252

# ============================================================
# 3. 计算滚动年化夏普比率
# ============================================================
# 超额收益（日度）
excess_returns = fund_returns - risk_free_rate_daily

# 滚动计算：窗口内超额收益均值 / 窗口内超额收益标准差，再年化
rolling_mean = excess_returns.rolling(window=window).mean()
rolling_std = excess_returns.rolling(window=window).std()

# 年化夏普比率 = (日度均值 * 252) / (日度标准差 * sqrt(252))
#             = (日度均值 / 日度标准差) * sqrt(252)
rolling_sharpe_annual = (rolling_mean / rolling_std) * np.sqrt(252)

# 去除前 window-1 个 NaN 值
rolling_sharpe_annual = rolling_sharpe_annual.dropna()

# ============================================================
# 4. 报告最后一个窗口的夏普值
# ============================================================
rolling_sharpe_last = rolling_sharpe_annual.iloc[-1]
print(f"最后一个 {window} 日窗口的年化夏普比率: {rolling_sharpe_last:.4f}")

# ============================================================
# 5. 绘制时间序列图
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(rolling_sharpe_annual.index, rolling_sharpe_annual.values, 
        linewidth=1.5, color='#2c3e50', label=f'{window}-Day Rolling Annualized Sharpe')

# 添加零线
ax.axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1)

# 标注最后一个值
ax.scatter(rolling_sharpe_annual.index[-1], rolling_sharpe_last, 
           color='#e74c3c', s=80, zorder=5)
ax.annotate(f'{rolling_sharpe_last:.3f}', 
            xy=(rolling_sharpe_annual.index[-1], rolling_sharpe_last),
            xytext=(10, 10), textcoords='offset points',
            fontsize=11, fontweight='bold', color='#e74c3c',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# 图表装饰
ax.set_title(f'Fund Rolling {window}-Day Annualized Sharpe Ratio\n(Risk-Free Rate = {risk_free_rate_annual*100:.1f}%)', 
             fontsize=14, fontweight='bold')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_facecolor('#f8f9fa')
fig.tight_layout()

# 保存图形
figure_path = 'rolling_sharpe_ratio.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"图形已保存至: {figure_path}")

# ============================================================
# 6. 输出结果字典
# ============================================================
result = {
    'rolling_sharpe_last': float(rolling_sharpe_last),
    'figure_path': os.path.abspath(figure_path)
}

print("\n" + "="*50)
print("结果字典:")
print(f"  rolling_sharpe_last: {result['rolling_sharpe_last']:.6f}")
print(f"  figure_path: {result['figure_path']}")
print("="*50)
