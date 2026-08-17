import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========== 参数设置（可调整）==========
window = 60          # 滚动窗口，可调
rf = 0.021           # 无风险利率 2.1%
# ====================================

# 假设 df 已经存在，包含 'fund' 列，索引为日期
# df = pd.read_csv('your_data.csv', index_col=0, parse_dates=True)

# 计算日收益率
returns = df['fund'].pct_change().dropna()

# 滚动年化收益率与波动率
roll_mean = returns.rolling(window).mean() * 252
roll_std = returns.rolling(window).std() * np.sqrt(252)

# 滚动夏普比率
rolling_sharpe = (roll_mean - rf) / roll_std

# 最后一个窗口的值
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# 绘制滚动夏普曲线
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe, label=f'{window}-Day Rolling Sharpe', color='b')
plt.axhline(y=0, color='r', linestyle='--', linewidth=1)
plt.title(f'Rolling Sharpe Ratio ({window}-day window, rf={rf*100}%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.tight_layout()
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# 按要求输出字典
result = {
    'rolling_sharpe_last': round(rolling_sharpe_last, 6),
    'figure_path': figure_path
}

print(result)
