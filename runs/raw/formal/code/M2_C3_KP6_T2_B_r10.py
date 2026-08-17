import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 读取数据
df = pd.read_csv('data.csv', index_col=0, parse_dates=True)

# 参数设置
window = 60
rf_annual = 0.021  # 2.1% 年化无风险利率
trading_days = 252

# 计算日无风险利率（连续复利转日度）
rf_daily = (1 + rf_annual) ** (1/trading_days) - 1

# 计算日收益率
returns = df['fund'].pct_change().dropna()

# 计算滚动夏普比率
# 先计算超额收益
excess_returns = returns - rf_daily

# 滚动计算年化夏普比率
rolling_mean = excess_returns.rolling(window=window).mean() * trading_days  # 年化超额收益
rolling_std = excess_returns.rolling(window=window).std(ddof=1) * np.sqrt(trading_days)  # 年化标准差
rolling_sharpe = rolling_mean / rolling_std

# 获取最后一个窗口值
rolling_sharpe_last = rolling_sharpe.iloc[-1]

print(f"最后一个窗口的滚动夏普比率: {rolling_sharpe_last:.4f}")

# 绘制图形
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# 上图：基金净值走势
ax1.plot(df.index, df['fund'], linewidth=1.5)
ax1.set_title('基金净值走势', fontsize=14)
ax1.set_ylabel('净值')
ax1.grid(True, alpha=0.3)
ax1.legend(['基金净值'])

# 下图：滚动夏普比率
ax2.plot(rolling_sharpe.index, rolling_sharpe.values, linewidth=1.5, color='darkblue')
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax2.axhline(y=rolling_sharpe_last, color='red', linestyle='--', linewidth=1, alpha=0.7, 
            label=f'最后值: {rolling_sharpe_last:.4f}')
ax2.set_title(f'{window}天滚动年化夏普比率 (无风险利率={rf_annual*100:.1f}%)', fontsize=14)
ax2.set_xlabel('日期')
ax2.set_ylabel('夏普比率')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# 保存图形
figure_path = 'rolling_sharpe_ratio.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.show()

print(f"\n图形已保存至: {figure_path}")

# 创建结果字典
result = {
    'rolling_sharpe_last': round(rolling_sharpe_last, 6),
    'figure_path': os.path.abspath(figure_path)
}

print(f"\n结果字典:")
print(f"rolling_sharpe_last: {result['rolling_sharpe_last']}")
print(f"figure_path: {result['figure_path']}")
