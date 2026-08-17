import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ========================
# 可调参数
# ========================
CSV_PATH = 'data/market_snapshot_v1.csv'   # 数据文件路径
RISK_FREE_RATE = 0.021                     # 年化无风险利率
WINDOW = 60                                # 滚动窗口长度（交易日数）
TRADING_DAYS = 252                         # 每年交易日数
OUTPUT_FIG = 'rolling_sharpe.png'          # 输出图形文件名

# ========================
# 1. 读取数据
# ========================
df = pd.read_csv(CSV_PATH)

# 若存在日期列则设为索引，否则保持默认索引
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
elif 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')

# 提取基金日收益率序列
fund_ret = df['fund']   # 小数形式，如 0.001 表示 0.1%

# 日化无风险利率
rf_daily = RISK_FREE_RATE / TRADING_DAYS

# 超额收益
excess_ret = fund_ret - rf_daily

# ========================
# 2. 计算 60 日滚动年化夏普比率
# ========================
roll_mean = excess_ret.rolling(window=WINDOW).mean()
roll_std  = excess_ret.rolling(window=WINDOW).std(ddof=1)   # 样本标准差
rolling_sharpe = np.sqrt(TRADING_DAYS) * (roll_mean / roll_std)

# 去掉 NaN 后的序列
rolling_sharpe_clean = rolling_sharpe.dropna()

# 3. 最后一个窗口的夏普值
rolling_sharpe_last = float(rolling_sharpe_clean.iloc[-1])

# ========================
# 4. 绘图并保存
# ========================
fig, ax = plt.subplots(figsize=(12, 5))
rolling_sharpe_clean.plot(ax=ax, linewidth=1.2, color='#1f77b4')
ax.set_title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('Sharpe Ratio')
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(OUTPUT_FIG, dpi=150)
plt.close(fig)   # 释放内存

# ========================
# 5. 封装结果
# ========================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': OUTPUT_FIG
}

# 打印结果以便教师查看
print('=== 输出结果 ===')
print(f"最后一个 {WINDOW} 日滚动年化夏普比率: {rolling_sharpe_last:.4f}")
print(f"图形已保存至: {OUTPUT_FIG}")
print('================')
print(result)
