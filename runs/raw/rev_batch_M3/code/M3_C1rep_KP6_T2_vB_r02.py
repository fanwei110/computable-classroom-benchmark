import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------ 1. 模拟数据准备 (如果有真实数据，直接替换df即可) ------------------
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=200, freq='D')
# 模拟一份基金净值数据
nav = [1.0]
for r in np.random.normal(0.0005, 0.02, 199):
    nav.append(nav[-1] * (1 + r))
df = pd.DataFrame({'fund': nav}, index=dates)

# ------------------ 2. 参数设置 ------------------
rf_annual = 0.021           # 年化无风险利率 2.1%
window = 60                 # 可调窗口大小，默认60天
rf_daily = rf_annual / 252  # 日无风险利率

# ------------------ 3. 计算滚动夏普 ------------------
# 计算日收益率
df['daily_return'] = df['fund'].pct_change()

# 计算滚动均值与滚动标准差
rolling_mean = df['daily_return'].rolling(window=window).mean()
rolling_std = df['daily_return'].rolling(window=window).std()

# 计算年化滚动夏普比率
rolling_sharpe = ((rolling_mean - rf_daily) / rolling_std) * np.sqrt(252)

# 获取最后一个窗口的值
rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]

# ------------------ 4. 绘图与保存 ------------------
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.dropna(), label=f'{window}-Day Rolling Sharpe', color='blue')
plt.axhline(0, color='red', linestyle='--', alpha=0.5)
plt.title(f'{window}-Day Rolling Sharpe Ratio (rf={rf_annual*100}%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.grid(alpha=0.3)

# 保存图片
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ------------------ 5. 按照输出契约构造结果字典 ------------------
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

# 打印结果查看
print(result)
