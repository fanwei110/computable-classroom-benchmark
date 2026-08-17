import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ================= 1. 准备数据 =================
# 模拟数据（实际使用时请替换为您的真实DataFrame）
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=300, freq='B')
returns = np.random.normal(0.001, 0.015, size=len(dates))
fund = 1000 * (1 + returns).cumprod()
df = pd.DataFrame({'date': dates, 'fund': fund}).set_index('date')

# ================= 2. 参数设置 =================
rf = 0.021          # 无风险利率 2.1%
window = 60         # 滚动窗口，可调（如改为120等）

# ================= 3. 计算滚动年化夏普 =================
# 计算日收益率
daily_returns = df['fund'].pct_change()

# 计算滚动均值与滚动标准差
rolling_mean = daily_returns.rolling(window=window).mean()
rolling_std = daily_returns.rolling(window=window).std()

# 年化夏普比率公式：(滚动均值 * 252 - rf) / (滚动标准差 * sqrt(252))
# 等价于：((rolling_mean - rf/252) / rolling_std) * sqrt(252)
rolling_sharpe = (rolling_mean * 252 - rf) / (rolling_std * np.sqrt(252))

# 获取最后一个窗口的数值
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# ================= 4. 绘制曲线 =================
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.index, rolling_sharpe, label=f'{window}-Day Rolling Sharpe (rf={rf*100}%)', color='blue')
plt.axhline(0, color='red', linestyle='--', linewidth=0.8)
plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.grid(True, alpha=0.3)

# 保存图片
fig_path = 'rolling_sharpe.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 5. 输出契约 =================
result = {
    'rolling_sharpe_last': float(rolling_sharpe_last),
    'figure_path': fig_path
}

print(result)
