import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 参数设定 (窗口长度可调)
# ==========================================
WINDOW = 60                 # 滚动窗口长度(交易日)
RF_ANNUAL = 0.021           # 年化无风险利率 2.1%
TRADING_DAYS = 252          # 一年的交易日数
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'rolling_sharpe_ratio.png'

# ==========================================
# 1. 读取快照 CSV；计入无风险利率
# ==========================================
# 读取数据
df = pd.read_csv(DATA_PATH)

# 提取基金日收益率列
fund_returns = df['fund']

# 计算日无风险利率 (按单利近似折算，与业界日度超额收益计算习惯一致)
rf_daily = RF_ANNUAL / TRADING_DAYS

# 计算日超额收益
excess_returns = fund_returns - rf_daily

# ==========================================
# 2. 计算 60 日滚动年化夏普，窗口可调
# ==========================================
# 计算滚动均值与滚动标准差 (ddof=1 为样本标准差，pandas默认值)
rolling_mean = excess_returns.rolling(window=WINDOW).mean()
rolling_std = excess_returns.rolling(window=WINDOW).std(ddof=1)

# 计算滚动日夏普比率并年化
# 年化夏普 = (日均值 / 日标准差) * sqrt(年交易日)
rolling_sharpe_annualized = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS)

# ==========================================
# 3. 报告最后一个窗口的值；画出时间序列
# ==========================================
# 提取最后一个有效窗口的夏普值
rolling_sharpe_last = rolling_sharpe_annualized.dropna().iloc[-1]

# 画图
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe_annualized, label=f'{WINDOW}-Day Rolling Annualized Sharpe Ratio', color='tab:blue')
plt.axhline(y=0, color='tab:red', linestyle='--', linewidth=1, alpha=0.8)

plt.title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio (Rf={RF_ANNUAL*100:.1f}%)', fontsize=14)
plt.xlabel('Date / Observation', fontsize=12)
plt.ylabel('Annualized Sharpe Ratio', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
plt.savefig(FIGURE_PATH, dpi=150, bbox_inches='tight')
plt.close()

# 填充结果字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH
}

# 课堂投屏辅助打印
print(f"最后一个 {WINDOW} 日窗口的年化夏普比率: {rolling_sharpe_last:.4f}")
print(f"图表已保存至: {FIGURE_PATH}")
