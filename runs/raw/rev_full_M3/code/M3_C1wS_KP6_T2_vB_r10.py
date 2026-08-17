import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 0. 自包含数据生成 (模拟快照 CSV)
# 为了确保代码完全自包含且可复现，此处先生成模拟的 snapshot.csv
# 假设 fund 列为基金日单位净值，共生成 200 个交易日数据
# ==========================================
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=200, freq='B')
nav = [1.0]
for _ in range(199):
    # 模拟日收益率：均值0.05%，标准差1.5%
    daily_ret = np.random.normal(0.0005, 0.015)
    nav.append(nav[-1] * (1 + daily_ret))

mock_df = pd.DataFrame({'date': dates, 'fund': nav})
mock_df.to_csv('snapshot.csv', index=False)

# ==========================================
# 1. 读取快照 CSV；计入无风险利率
# ==========================================
df = pd.read_csv('snapshot.csv', parse_dates=['date'])
df.sort_values('date', inplace=True)
df.reset_index(drop=True, inplace=True)

# 假设：无风险利率 rf = 2.1% 为年化利率
# 假设：一年按 252 个交易日计算，日化无风险利率
rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days

# 计算基金日简单收益率 (假设 fund 列为净值)
df['daily_return'] = df['fund'].pct_change()

# 计算日超额收益
df['excess_return'] = df['daily_return'] - rf_daily

# ==========================================
# 2. 计算 60 日滚动年化夏普，窗口可调
# ==========================================
# 窗口大小可调参数
window = 60

# 计算滚动均值与标准差
rolling_mean = df['excess_return'].rolling(window=window).mean()
rolling_std = df['excess_return'].rolling(window=window).std()

# 年化滚动夏普比率 = (日超额收益均值 / 日超额收益标准差) * sqrt(252)
# 避免除以0：若标准差为0，夏普设为0
df['rolling_sharpe'] = np.where(
    rolling_std == 0, 
    0, 
    (rolling_mean / rolling_std) * np.sqrt(trading_days)
)

# ==========================================
# 3. 报告最后一个窗口的值；画出时间序列
# ==========================================
# 提取最后一个窗口的夏普比率值
rolling_sharpe_last = df['rolling_sharpe'].iloc[-1]

# 打印最后一个窗口的值以便课堂展示
print(f"最后一个窗口({window}日)的滚动年化夏普比率为: {rolling_sharpe_last:.4f}")

# 画图
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['date'], df['rolling_sharpe'], label=f'{window}-Day Rolling Annualized Sharpe', color='tab:blue')
ax.axhline(y=0, color='tab:red', linestyle='--', linewidth=1, label='Zero Line')
ax.set_title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf={rf_annual*100}%)', fontsize=14)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Sharpe Ratio', fontsize=12)
ax.legend()
ax.grid(True, linestyle=':', alpha=0.7)

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
figure_path = 'rolling_sharpe.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# 按照输出契约填充字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}
