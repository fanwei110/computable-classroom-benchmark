import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ================= 1. 准备数据 (如果你有自己的数据，直接替换这部分即可) =================
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=250, freq='D')
# 模拟一个基金净值序列
nav = (1 + np.random.normal(0.0004, 0.015, 250)).cumprod() * 1.0
df = pd.DataFrame({'date': dates, 'fund': nav})
df.set_index('date', inplace=True)

# ================= 2. 参数设置 =================
rf_annual = 0.021            # 年化无风险利率 2.1%
window_size = 60             # 滚动窗口大小（可在此处调整）

# ================= 3. 计算滚动夏普 =================
# 计算日度收益率
df['daily_return'] = df['fund'].pct_change()

# 计算日度无风险利率
rf_daily = rf_annual / 252

# 计算超额收益
df['excess_return'] = df['daily_return'] - rf_daily

# 计算滚动均值和滚动标准差
rolling_mean = df['excess_return'].rolling(window=window_size).mean()
rolling_std = df['excess_return'].rolling(window=window_size).std()

# 年化滚动夏普比率
df['rolling_sharpe'] = (rolling_mean / rolling_std) * np.sqrt(252)

# 提取最后一个窗口的值（去除NaN）
last_valid_sharpe = df['rolling_sharpe'].dropna().iloc[-1]

# ================= 4. 绘图并保存 =================
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['rolling_sharpe'], label=f'{window_size}-Day Rolling Sharpe', color='royalblue')
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
plt.title(f'{window_size}-Day Rolling Sharpe Ratio (rf={rf_annual*100}%)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Annualized Sharpe Ratio', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()

# 保存图片
figure_path = 'rolling_sharpe_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ================= 5. 按照输出契约构建字典 =================
result = {
    'rolling_sharpe_last': last_valid_sharpe,
    'figure_path': os.path.abspath(figure_path)
}

# 打印结果查看
print(f"最后一个窗口的滚动夏普值: {result['rolling_sharpe_last']:.4f}")
print(f"图片已保存至: {result['figure_path']}")
