import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ========================
# 可调参数
# ========================
WINDOW = 60                # 滚动窗口（交易日）
RISK_FREE_RATE = 0.021     # 年化无风险利率
ANNUAL_FACTOR = 252        # 年化因子（假设一年252个交易日）

# ========================
# 1. 读取数据
# ========================
DATA_PATH = 'data/market_snapshot_v1.csv'
df = pd.read_csv(DATA_PATH)

# 自动识别日期列（常见列名：date, Date, DATE, timestamp）
date_col = None
for col in df.columns:
    if col.lower() in ['date', 'timestamp', 'time', 'day']:
        date_col = col
        break
if date_col is None:
    # 若无日期列，假定数据已按时间顺序排列，生成序号作为索引
    df['_idx_'] = range(len(df))
    date_col = '_idx_'
    print("Warning: No date column found. Using row index as time axis.")
else:
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    df = df.sort_values(by=date_col).reset_index(drop=True)

# 确保存在 'fund' 列
if 'fund' not in df.columns:
    raise ValueError("CSV文件缺少 'fund' 列。请检查列名。")

# ========================
# 2. 计算日超额收益
# ========================
daily_rf = RISK_FREE_RATE / ANNUAL_FACTOR
df['excess_return'] = df['fund'] - daily_rf

# ========================
# 3. 滚动年化夏普比率
# ========================
rolling_mean = df['excess_return'].rolling(window=WINDOW).mean()
rolling_std = df['excess_return'].rolling(window=WINDOW).std()
df['rolling_sharpe'] = (rolling_mean / rolling_std) * np.sqrt(ANNUAL_FACTOR)

# 获取最后一个窗口的值（剔除可能的NaN）
sharpe_series = df['rolling_sharpe'].dropna()
if len(sharpe_series) == 0:
    rolling_sharpe_last = np.nan
    print("Warning: 数据不足一个窗口长度，无法计算滚动夏普比率。")
else:
    rolling_sharpe_last = sharpe_series.iloc[-1]

# ========================
# 4. 绘图并保存
# ========================
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df[date_col], df['rolling_sharpe'], color='steelblue', linewidth=1.2, label='60-Day Rolling Sharpe')
ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
ax.set_title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio (rf={RISK_FREE_RATE*100:.1f}%)')
ax.set_xlabel('Date' if date_col != '_idx_' else 'Index')
ax.set_ylabel('Annualized Sharpe Ratio')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()

FIG_PATH = 'sharpe_ratio_rolling.png'
fig.savefig(FIG_PATH, dpi=150)
plt.close(fig)

# ========================
# 5. 输出结果字典
# ========================
result = {
    'rolling_sharpe_last': round(float(rolling_sharpe_last), 6) if not np.isnan(rolling_sharpe_last) else None,
    'figure_path': os.path.abspath(FIG_PATH)
}

if __name__ == '__main__':
    print("Result:")
    for k, v in result.items():
        print(f"  {k}: {v}")
