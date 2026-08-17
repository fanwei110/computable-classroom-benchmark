import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 假设与参数设置
# ==========================================
ANNUAL_RF = 0.021          # 年化无风险利率 2.1%
TRADING_DAYS = 252         # 一年交易日天数，用于年化
WINDOW = 60                # 滚动窗口长度（可调参数）
FIGURE_PATH = 'rolling_sharpe_ratio.png'
CSV_PATH = 'data/market_snapshot_v1.csv'

# ==========================================
# 1. 读取快照 CSV；计入无风险利率
# ==========================================
df = pd.read_csv(CSV_PATH)
daily_returns = df['fund'].astype(float)

# 计算日无风险利率（通常采用单利折算日度）
daily_rf = ANNUAL_RF / TRADING_DAYS

# 计算日超额收益
excess_returns = daily_returns - daily_rf

# ==========================================
# 2. 计算 60 日滚动年化夏普，窗口可调
# ==========================================
# 使用 pandas 内置 rolling 计算滚动均值与标准差
# ddof=1 为 pandas 默认设置，计算样本标准差，符合金融惯例
rolling_mean = excess_returns.rolling(window=WINDOW).mean()
rolling_std = excess_returns.rolling(window=WINDOW).std()

# 年化滚动夏普比率 = (日均超额收益 / 日收益标准差) * sqrt(252)
rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS)

# ==========================================
# 3. 报告最后一个窗口的值；画出时间序列
# ==========================================
# 提取最后一个完整的滚动窗口计算结果
# 如果末尾存在 NaN（数据长度不足一个窗口），则取最后一个非 NaN 值
last_valid_sharpe = rolling_sharpe.dropna().iloc[-1]
rolling_sharpe_last = float(last_valid_sharpe)

# 绘制时间序列图
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe, color='tab:blue', label=f'{WINDOW}-Day Rolling Sharpe')
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.7)
plt.title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio (Rf = {ANNUAL_RF*100:.1f}%)', fontsize=14)
plt.xlabel('Date / Observation Index', fontsize=12)
plt.ylabel('Annualized Sharpe Ratio', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(fontsize=11)

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
plt.tight_layout()
plt.savefig(FIGURE_PATH, dpi=150)
plt.close()

# 按照输出契约存储结果
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH
}
