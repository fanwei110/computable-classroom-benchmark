import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==================== 假设与参数配置 ====================
# 滚动窗口长度，设为可调变量
WINDOW = 60
# 年化无风险利率
RF_ANNUAL = 0.021
# 一年中的交易日天数（用于日度数据年化）
TRADING_DAYS = 252
# 数据文件路径
DATA_PATH = 'data/market_snapshot_v1.csv'
# 图形保存路径
FIGURE_PATH = 'rolling_sharpe_ratio.png'

# ==================== 1. 读取快照 CSV ====================
df = pd.read_csv(DATA_PATH)

# 尝试解析日期列为索引，以支持时间序列绘图
date_col = None
for col in df.columns:
    if 'date' in col.lower():
        date_col = col
        break

if date_col:
    df[date_col] = pd.to_datetime(df[date_col])
    df.set_index(date_col, inplace=True)

# ==================== 2. 计算 60 日滚动年化夏普 ====================
# 日度无风险利率（采用简单除法进行日化，与行业惯例一致且便于日收益相减）
rf_daily = RF_ANNUAL / TRADING_DAYS

# 提取基金日收益率
fund_returns = df['fund']

# 计算日超额收益
excess_returns = fund_returns - rf_daily

# 计算滚动均值与滚动标准差
# 标准差使用总收益的标准差（因无风险利率恒定，总风险与超额收益风险一致）
rolling_mean_excess = excess_returns.rolling(window=WINDOW).mean()
rolling_std_total = fund_returns.rolling(window=WINDOW).std()

# 计算日度夏普比率并年化
# 年化夏普 = 日度夏普 * sqrt(252)
rolling_sharpe_annualized = (rolling_mean_excess / rolling_std_total) * np.sqrt(TRADING_DAYS)

# ==================== 3. 报告最后一个窗口的值并绘图 ====================
# 提取最后一个窗口的夏普值
rolling_sharpe_last = rolling_sharpe_annualized.iloc[-1]

# 绘制时间序列图
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe_annualized.index, rolling_sharpe_annualized.values, 
         label=f'{WINDOW}-Day Rolling Annualized Sharpe', color='tab:blue', linewidth=1.2)

plt.title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio (Rf = {RF_ANNUAL*100:.1f}%)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.7)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=11)
plt.tight_layout()

# ==================== 4. 保存图形并填充 result ====================
plt.savefig(FIGURE_PATH, dpi=150)
plt.close()

# 按照输出契约构造字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH
}
