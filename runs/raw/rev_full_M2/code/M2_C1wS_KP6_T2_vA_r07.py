import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# ========================
# 可调参数
# ========================
WINDOW = 60                 # 滚动窗口（交易日数）
ANNUAL_RF = 0.021           # 年化无风险利率
TRADING_DAYS = 252          # 年交易日数

# ========================
# 1. 读取快照 CSV
# ========================
# 用法: python script.py [data.csv]
# 若不提供命令行参数，默认读取 ./data.csv
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = 'data.csv'

df = pd.read_csv(file_path, parse_dates=['date'])
df = df.sort_values('date').reset_index(drop=True)

# 假设 fund 列为日净值，计算日收益率
df['return'] = df['fund'].pct_change()

# ========================
# 2. 计算 60 日滚动年化夏普
# ========================
def rolling_annual_sharpe(rets, window, rf_annual):
    """返回滚动年化夏普序列"""
    roll_mean = rets.rolling(window, min_periods=window).mean()
    roll_std  = rets.rolling(window, min_periods=window).std()
    ann_ret = roll_mean * TRADING_DAYS
    ann_vol = roll_std * np.sqrt(TRADING_DAYS)
    sharpe = (ann_ret - rf_annual) / ann_vol
    return sharpe

df['sharpe'] = rolling_annual_sharpe(df['return'], WINDOW, ANNUAL_RF)

# ========================
# 3. 最后一个窗口的值
# ========================
last_sharpe = df['sharpe'].iloc[-1]
rolling_sharpe_last = float(last_sharpe)
print(f"最后一个窗口 (window={WINDOW}) 的年化夏普: {rolling_sharpe_last:.4f}")

# ========================
# 4. 绘制时间序列并保存
# ========================
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df['date'], df['sharpe'], color='navy', linewidth=0.8, label=f'{WINDOW}-Day Rolling Annualized Sharpe')
ax.axhline(0, color='gray', linestyle='--', linewidth=0.7)
ax.set_title(f'Rolling Annualized Sharpe Ratio (rf={ANNUAL_RF*100:.1f}%)', fontsize=13)
ax.set_xlabel('Date')
ax.set_ylabel('Sharpe Ratio')
ax.legend()
fig.autofmt_xdate()
plt.tight_layout()

figure_path = os.path.abspath('rolling_sharpe.png')
fig.savefig(figure_path, dpi=150)
plt.close()

# ========================
# 输出契约
# ========================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

# 打印供教师查阅
print("\n输出结果:")
print(result)
