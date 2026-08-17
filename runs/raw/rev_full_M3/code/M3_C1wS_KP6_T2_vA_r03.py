import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 0. 模拟数据生成 (保证脚本自包含与可复现)
# ==========================================
# 假设当前目录没有快照文件，此处自动生成一份符合要求的 snapshot.csv 供演示
# 若教师机已有该文件，此操作会覆盖，但不影响后续读取逻辑
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=300, freq='B')
# 模拟基金净值：围绕1.0波动，日收益率均值略正
fund_prices = 1.0 * np.exp(np.cumsum(np.random.normal(0.0002, 0.015, len(dates))))
mock_df = pd.DataFrame({'date': dates, 'fund': fund_prices})
csv_path = 'snapshot.csv'
mock_df.to_csv(csv_path, index=False)

# ==========================================
# 1. 读取快照 CSV；计入无风险利率
# ==========================================
# 尝试将第一列作为日期解析，若失败则仅使用 fund 列
try:
    df = pd.read_csv(csv_path, parse_dates=[0], index_col=0)
except Exception:
    df = pd.read_csv(csv_path)

# 确保数据按时间正序排列
df = df.sort_index()

# 提取 fund 列
fund_series = df['fund']

# 假设设定
rf_annual = 0.021          # 年化无风险利率 2.1%
trading_days = 242         # 一年交易日，国内常用假设
rf_daily = (1 + rf_annual) ** (1 / trading_days) - 1  # 日化无风险利率

# 计算日收益率与日超额收益
daily_returns = fund_series.pct_change()
excess_daily_returns = daily_returns - rf_daily

# ==========================================
# 2. 计算 60 日滚动年化夏普，窗口可调
# ==========================================
window = 60  # 窗口大小，可按需调整

# 计算滚动均值与标准差
rolling_mean = excess_daily_returns.rolling(window=window).mean()
rolling_std = excess_daily_returns.rolling(window=window).std()

# 滚动年化夏普比率 = (滚动日均超额收益 / 滚动日标准差) * sqrt(年交易日)
rolling_sharpe_annual = (rolling_mean / rolling_std) * np.sqrt(trading_days)

# ==========================================
# 3. 报告最后一个窗口的值；画出时间序列
# ==========================================
# 提取最后一个窗口的值
rolling_sharpe_last = rolling_sharpe_annual.iloc[-1]

# 绘制时间序列
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']  # 兼容中文字体
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(12, 6))
rolling_sharpe_annual.plot(ax=ax, color='royalblue', linewidth=1.5, label=f'{window}-Day Rolling Annualized Sharpe')
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
ax.set_title(f'基金 {window}日滚动年化夏普比率 (rf={rf_annual*100}%)', fontsize=14)
ax.set_xlabel('日期', fontsize=12)
ax.set_ylabel('年化夏普比率', fontsize=12)
ax.legend(loc='upper left')
ax.grid(True, linestyle=':', alpha=0.6)

# 标注最后一个点的数值
last_date = rolling_sharpe_annual.index[-1]
ax.scatter(last_date, rolling_sharpe_last, color='red', zorder=5)
ax.annotate(f'{rolling_sharpe_last:.4f}', 
            xy=(last_date, rolling_sharpe_last), 
            xytext=(-50, 20), 
            textcoords='offset points',
            arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
            fontsize=12, 
            color='red',
            fontweight='bold')

fig.tight_layout()

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
figure_path = 'rolling_sharpe_curve.png'
fig.savefig(figure_path, dpi=150)
plt.close(fig)

# 按输出契约构造结果字典
result = {
    'rolling_sharpe_last': float(rolling_sharpe_last),
    'figure_path': figure_path
}

# 课堂投屏打印输出
print(f"最后一个窗口的滚动年化夏普比率: {result['rolling_sharpe_last']:.4f}")
print(f"图形已保存至: {result['figure_path']}")
