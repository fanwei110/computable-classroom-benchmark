import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------------------
# 可调参数
# ------------------------------
WINDOW = 60               # 滚动窗口（天）
RF_YEARLY = 0.021         # 年化无风险利率
TRADING_DAYS = 252        # 一年交易天数
DATA_FILE = 'data.csv'    # 输入数据文件（需包含至少 date 和 fund 列）

# ------------------------------
# 1. 读取数据并计算日收益率
# ------------------------------
df = pd.read_csv(DATA_FILE, parse_dates=['date'])
df.sort_values('date', inplace=True)
df.set_index('date', inplace=True)

# 假设 fund 列为净值，计算日简单收益率（若已经是收益率则直接使用）
# 自动判断：若数值范围在 0~0.1 附近为收益率，否则按净值处理
if df['fund'].abs().max() < 0.5:
    returns = df['fund'].copy()
else:
    returns = df['fund'].pct_change().dropna()

# ------------------------------
# 2. 计算滚动年化夏普比率
# ------------------------------
rf_daily = RF_YEARLY / TRADING_DAYS

# 滚动均值和滚动标准差（窗口至少为 WINDOW）
roll_mean = returns.rolling(window=WINDOW).mean()
roll_std = returns.rolling(window=WINDOW).std()

# 年化
ann_return = roll_mean * TRADING_DAYS
ann_vol = roll_std * np.sqrt(TRADING_DAYS)

rolling_sharpe = (ann_return - RF_YEARLY) / ann_vol

# ------------------------------
# 3. 获取最后一个窗口的夏普值
# ------------------------------
rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]

# ------------------------------
# 4. 画图并保存
# ------------------------------
fig_path = 'sharpe_ratio.png'
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe.index, rolling_sharpe, color='navy', linewidth=1.2)
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
plt.title(f'{WINDOW}-Day Rolling Sharpe Ratio (rf={RF_YEARLY*100:.1f}%)')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.tight_layout()
plt.savefig(fig_path, dpi=150)
plt.close()

# ------------------------------
# 5. 构造输出字典
# ------------------------------
result = {
    'rolling_sharpe_last': round(rolling_sharpe_last, 6),
    'figure_path': fig_path
}

# 仅供查看，实际环境会使用该字典
print(result)
