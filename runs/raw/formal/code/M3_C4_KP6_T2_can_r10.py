import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ===== 配置参数 =====
csv_path = 'data/market_snapshot_v1.csv'
annual_rf_rate = 0.021       # 年化无风险利率 2.1%
window = 60                  # 滚动窗口长度（可调）
output_fig_path = 'rolling_sharpe_ratio.png'

# ===== 1. 读取快照 CSV；日无风险利率取年利率/252 =====
df = pd.read_csv(csv_path)
daily_returns = df['fund']
daily_rf = annual_rf_rate / 252  # 日无风险利率

# ===== 2. 计算 60 日滚动夏普（ddof=1），按 sqrt(252) 年化，窗口可调 =====
# 计算日超额收益
excess_returns = daily_returns - daily_rf

# 计算滚动均值与滚动标准差（样本标准差 ddof=1）
rolling_mean = excess_returns.rolling(window=window).mean()
rolling_std = excess_returns.rolling(window=window).std(ddof=1)

# 年化夏普比率 = (平均超额收益 / 超额收益标准差) * sqrt(252)
# 等价于：(滚动均值 * 252) / (滚动标准差 * sqrt(252))
rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

# ===== 3. 报告最后一个窗口的值（小数）；画出时间序列 =====
# 剔除前期无足够数据的 NaN，取最后一个值
rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]

# 绘制时间序列图
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(rolling_sharpe.dropna().index, rolling_sharpe.dropna().values, 
        label=f'{window}-Day Rolling Annualized Sharpe', color='tab:blue')
ax.set_title(f'{window}-Day Rolling Annualized Sharpe Ratio')
ax.set_xlabel('Trading Days')
ax.set_ylabel('Annualized Sharpe Ratio')
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

# ===== 4. 保存图形并填充 result =====
fig.savefig(output_fig_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# 按照输出契约组装结果字典
result = {
    'rolling_sharpe_last': float(rolling_sharpe_last),
    'figure_path': output_fig_path
}

# 供课堂投屏与检查使用
print(f"最后 60 日窗口的年化夏普比率: {result['rolling_sharpe_last']:.4f}")
print(f"图形已保存至: {result['figure_path']}")
