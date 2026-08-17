import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================
# 参数设置
# =========================
WINDOW = 60                     # 滚动窗口（交易日），可调
RISK_FREE_RATE_ANNUAL = 0.021   # 年化无风险利率
TRADING_DAYS = 252              # 年交易日数
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'rolling_sharpe.png'

# =========================
# 1. 读取数据
# =========================
df = pd.read_csv(DATA_PATH)

# 确保按照时间顺序排列（若存在日期列，自动排序；否则保持原序）
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values('date', inplace=True)
    df.reset_index(drop=True, inplace=True)

# 提取基金收益率列 (假设为小数形式；若为百分数则自动转换)
fund_returns = df['fund'].astype(float).copy()

# 自动检测：若大部分收益率的绝对值大于0.5，认为是百分比形式，转换为小数
if fund_returns.abs().median() > 0.5:
    fund_returns = fund_returns / 100.0

# 去除缺失值
fund_returns.dropna(inplace=True)

# 检查数据长度是否足够
if len(fund_returns) < WINDOW:
    raise ValueError(f"数据长度 {len(fund_returns)} 小于窗口长度 {WINDOW}，无法计算滚动夏普比率。")

# =========================
# 2. 计算日超额收益与滚动夏普
# =========================
rf_daily = RISK_FREE_RATE_ANNUAL / TRADING_DAYS
excess_returns = fund_returns - rf_daily

# 滚动计算年化夏普比率：(年化超额收益均值) / (年化波动率)
rolling_mean = excess_returns.rolling(window=WINDOW).mean() * TRADING_DAYS
rolling_std = excess_returns.rolling(window=WINDOW).std() * np.sqrt(TRADING_DAYS)
rolling_sharpe = rolling_mean / rolling_std

# =========================
# 3. 获取最后一个窗口的值
# =========================
rolling_sharpe_last = rolling_sharpe.iloc[-1]  # 最近一个完整窗口
# 防止 NaN（如果最后一个窗口全是 NaN，则向前寻找）
if pd.isna(rolling_sharpe_last):
    # 取最后一个有效值
    valid_sharpes = rolling_sharpe.dropna()
    if len(valid_sharpes) > 0:
        rolling_sharpe_last = valid_sharpes.iloc[-1]
    else:
        rolling_sharpe_last = np.nan

# =========================
# 4. 绘图并保存
# =========================
plt.figure(figsize=(10, 5))
plt.plot(rolling_sharpe.index, rolling_sharpe.values, label=f'{WINDOW}-Day Rolling Annualized Sharpe', color='navy')
plt.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
plt.title(f'Rolling Annualized Sharpe Ratio (Window={WINDOW} days)')
plt.xlabel('Time Index')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.tight_layout()
plt.savefig(FIGURE_PATH, dpi=150)
plt.close()

# =========================
# 5. 填充结果字典
# =========================
result = {
    'rolling_sharpe_last': float(rolling_sharpe_last),
    'figure_path': os.path.abspath(FIGURE_PATH)
}

# 输出结果供查看（可注释掉，此处保留以方便课堂投屏检查）
print("计算完成。结果字典：")
print(result)
