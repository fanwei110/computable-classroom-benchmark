import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 可调参数（课堂可根据需要修改）
# =========================
CSV_FILE = "snapshot.csv"   # 快照 CSV 文件路径
WINDOW = 60                 # 滚动窗口（交易日）
RF_ANNUAL = 0.021           # 年化无风险利率 2.1%
ANNUAL_FACTOR = 252         # 年化因子（假设 252 个交易日）

# =========================
# 1. 读取数据
# =========================
df = pd.read_csv(CSV_FILE)

# 确保存在 'fund' 列
if 'fund' not in df.columns:
    raise KeyError("CSV 文件中必须包含 'fund' 列")

# 处理日期索引
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
elif 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
else:
    # 若无日期列，自动生成交易日期索引（仅用于绘图美观）
    df = df.reset_index(drop=True)
    df.index = pd.date_range(start='2000-01-01', periods=len(df), freq='B')

fund_returns = df['fund'].astype(float).dropna()  # 去除空值，保持时间序列长度
if len(fund_returns) < WINDOW:
    raise ValueError(f"可用数据点 {len(fund_returns)} 少于窗口长度 {WINDOW}，无法计算")

# =========================
# 2. 计算滚动年化夏普比率
# =========================
rf_daily = RF_ANNUAL / ANNUAL_FACTOR          # 日化无风险利率
excess_returns = fund_returns - rf_daily

# 滚动计算
rolling_mean = excess_returns.rolling(window=WINDOW).mean()
rolling_std = excess_returns.rolling(window=WINDOW).std()
rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(ANNUAL_FACTOR)

# 3. 最后一个有效窗口的夏普值
valid_sharpe = rolling_sharpe.dropna()
rolling_sharpe_last = valid_sharpe.iloc[-1] if not valid_sharpe.empty else np.nan

# =========================
# 4. 绘图并保存
# =========================
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(rolling_sharpe.index, rolling_sharpe.values,
        color='#1f77b4', linewidth=1.2, label=f'{WINDOW}-Day Rolling Sharpe')
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title(f'Rolling {WINDOW}-Day Annualized Sharpe Ratio', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('Sharpe Ratio')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()

figure_path = "rolling_sharpe.png"
fig.savefig(figure_path, dpi=150)
plt.close(fig)  # 释放内存

# =========================
# 5. 输出契约
# =========================
result = {
    'rolling_sharpe_last': round(float(rolling_sharpe_last), 6),
    'figure_path': figure_path
}

# 课堂运行可直接查看 result 字典
print(result)
