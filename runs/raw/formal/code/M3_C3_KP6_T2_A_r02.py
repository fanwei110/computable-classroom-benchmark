import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 参数设置
# ============================================================
rf_annual = 0.021          # 年化无风险利率 2.1%（年复利报价）
window = 60                # 滚动窗口（可调）
trading_days = 252         # 每年交易日

# ============================================================
# 读取数据 —— 请将 df 替换为您的实际数据
# df 需包含 'fund' 列（日收益率，小数表示，如 0.01 = 1%）
# ============================================================
# df = pd.read_csv('your_data.csv', parse_dates=['date'], index_col='date')
# 以下为示例占位，请替换为真实数据
# df = ...  

# ============================================================
# 核心计算
# ============================================================
# 年复利 -> 日复利
daily_rf = (1 + rf_annual) ** (1 / trading_days) - 1

# 日超额收益
excess_returns = df['fund'] - daily_rf

# 滚动均值 & 滚动标准差（ddof=1，样本估计量）
rolling_mean = excess_returns.rolling(window=window).mean()
rolling_std  = excess_returns.rolling(window=window).std(ddof=1)

# 滚动年化夏普 = (均值 × 252) / (标准差 × √252) = 均值 × √252 / 标准差
rolling_sharpe = rolling_mean * np.sqrt(trading_days) / rolling_std

# 最后一个窗口的数值
rolling_sharpe_last = float(rolling_sharpe.iloc[-1])

# ============================================================
# 绘图
# ============================================================
fig, ax = plt.subplots(figsize=(14, 5))
rolling_sharpe.plot(ax=ax, color='steelblue', linewidth=1.0,
                    label=f'{window}-Day Rolling Annualized Sharpe')
ax.axhline(y=0, color='grey', linestyle='--', linewidth=0.8)
ax.set_title(f'{window}-Day Rolling Annualized Sharpe Ratio  (rf={rf_annual*100}%)',
             fontsize=13)
ax.set_xlabel('Date')
ax.set_ylabel('Sharpe Ratio')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig('rolling_sharpe.png', dpi=150)
plt.close()

# ============================================================
# 输出
# ============================================================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': 'rolling_sharpe.png'
}

print(f"最后一个窗口的滚动年化夏普: {rolling_sharpe_last:.6f}")
print(f"图片已保存至: {result['figure_path']}")
