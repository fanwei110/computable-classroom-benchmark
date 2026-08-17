import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==================== 可调整参数 ====================
WINDOW = 60                 # 滚动窗口长度（可调）
ANNUALIZATION = 252         # 年化因子（交易日）
RISK_FREE_RATE = 0.021      # 年化无风险利率
# ===================================================

DAILY_RF = RISK_FREE_RATE / ANNUALIZATION   # 日化无风险利率

# 1. 读取快照 CSV，以日期作为索引，提取 fund 列日收益
df = pd.read_csv('data/market_snapshot_v1.csv',
                 parse_dates=['Date'],
                 index_col='Date')
fund_returns = df['fund']

# 2. 计算超额收益
excess_returns = fund_returns - DAILY_RF

def annualized_sharpe(series):
    """ 对一段超额日收益序列计算年化夏普比率 """
    if len(series) < 2:
        return np.nan
    mu = series.mean()
    sigma = series.std(ddof=1)          # 使用样本标准差
    if sigma == 0:
        return np.nan
    return (mu / sigma) * np.sqrt(ANNUALIZATION)

# 滚动计算
rolling_sharpe = excess_returns.rolling(window=WINDOW).apply(annualized_sharpe, raw=False)

# 3. 报告最后一个 60 日窗口的年化夏普值（若最后一窗为 NaN 则取最后一个有效值）
last_sharpe = rolling_sharpe.iloc[-1]
if np.isnan(last_sharpe):
    valid = rolling_sharpe.dropna()
    last_sharpe = valid.iloc[-1] if not valid.empty else np.nan

# 4. 绘图并保存
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe.index, rolling_sharpe,
         color='blue', linewidth=1, label=f'{WINDOW}-Day Rolling Annualized Sharpe')
plt.axhline(y=0, color='gray', linestyle='--')
plt.title(f'Rolling {WINDOW}-Day Annualized Sharpe Ratio (Fund)')
plt.xlabel('Date')
plt.ylabel('Annualized Sharpe Ratio')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

fig_path = 'rolling_sharpe_60d.png'
plt.savefig(fig_path, dpi=100)
plt.close()

# 输出契约：存入 result 字典
result = {
    'rolling_sharpe_last': float(last_sharpe),   # 确保可序列化
    'figure_path': fig_path
}

# 供教师实时查看（课堂投屏可直接展示此输出）
print(result)
