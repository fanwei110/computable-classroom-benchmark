import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 配置参数 ====================
WINDOW = 60  # 滚动窗口（可调）
RISK_FREE_RATE = 0.021  # 无风险利率 2.1%
ANNUALIZATION_FACTOR = 252  # 年化因子（交易日）

# ==================== 1. 读取数据 ====================
# 读取 CSV 文件
csv_path = 'snapshot.csv'  # 请确保文件在相同目录下
df = pd.read_csv(csv_path, parse_dates=['date'])
df.sort_values('date', inplace=True)
df.reset_index(drop=True, inplace=True)

# ==================== 2. 计算日收益率 ====================
# 假设 fund 列是基金净值，计算日简单收益率或对数收益率
# 这里使用简单收益率（也可换为对数收益率，内部一致即可）
df['daily_return'] = df['fund'].pct_change()

# 超额日收益
df['excess_return'] = df['daily_return'] - (RISK_FREE_RATE / ANNUALIZATION_FACTOR)

# ==================== 3. 滚动年化夏普比率 ====================
# 滚动计算超额收益的均值和标准差
rolling_mean = df['excess_return'].rolling(window=WINDOW).mean()
rolling_std = df['excess_return'].rolling(window=WINDOW).std()

# 年化夏普比率（将日均值和日标准差年化）
df['rolling_sharpe'] = (rolling_mean / rolling_std) * np.sqrt(ANNUALIZATION_FACTOR)

# ==================== 4. 最后一个窗口值 ====================
rolling_sharpe_last = df['rolling_sharpe'].iloc[-1]
print(f"滚动 {WINDOW} 天年化夏普比率最后一个窗口值: {rolling_sharpe_last:.6f}")

# ==================== 5. 绘制时间序列 ====================
fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(df['date'], df['rolling_sharpe'], 
         color='navy', linewidth=1.2, label=f'{WINDOW}-Day Rolling Annualized Sharpe Ratio')

ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
ax.fill_between(df['date'], 0, df['rolling_sharpe'], 
                where=(df['rolling_sharpe'] > 0), color='green', alpha=0.15, interpolate=True)
ax.fill_between(df['date'], 0, df['rolling_sharpe'], 
                where=(df['rolling_sharpe'] <= 0), color='red', alpha=0.15, interpolate=True)

ax.set_xlabel('Date')
ax.set_ylabel('Annualized Sharpe Ratio')
ax.set_title(f'Rolling {WINDOW}-Day Annualized Sharpe Ratio (Risk-Free Rate = 2.1%)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.xticks(rotation=30)
plt.tight_layout()

# 保存图形
figure_path = 'rolling_sharpe_ratio.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.show()
print(f"图形已保存至: {figure_path}")

# ==================== 结果汇总 ====================
result = {
    'rolling_sharpe_last': round(float(rolling_sharpe_last), 6),
    'figure_path': os.path.abspath(figure_path)
}

print("\n===== 输出字典 =====")
for key, value in result.items():
    print(f"'{key}': {value}")
