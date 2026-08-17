import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 0. 生成模拟快照 CSV (保证脚本自包含可运行)
# 如果当前目录已有 snapshot.csv，可注释掉此部分
# ==========================================
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=300, freq='B')
# 模拟基金净值：初始净值1.0，日均收益率约0.05%，日波动率约1.5%
sim_returns = np.random.normal(loc=0.0005, scale=0.015, size=len(dates))
sim_fund = 1.0 * (1 + sim_returns).cumprod()
mock_df = pd.DataFrame({'date': dates, 'fund': sim_fund})
csv_path = 'snapshot.csv'
mock_df.to_csv(csv_path, index=False)

# ==========================================
# 1. 读取快照 CSV；计入无风险利率
# ==========================================
df = pd.read_csv(csv_path, parse_dates=['date'])
df.sort_values('date', inplace=True)
df.set_index('date', inplace=True)

# 假设参数
rf_annual = 0.021          # 年化无风险利率 2.1%
trading_days = 252         # 一年交易日
window = 60                # 滚动窗口大小，可在此调整

# 计算日无风险利率 (常用简单除法或复利，此处采用简单除法以与日收益率匹配)
rf_daily = rf_annual / trading_days

# 计算基金日收益率
df['daily_return'] = df['fund'].pct_change()

# ==========================================
# 2. 计算 60 日滚动年化夏普
# ==========================================
# 日超额收益
df['excess_return'] = df['daily_return'] - rf_daily

# 滚动计算均值与标准差
rolling_mean_excess = df['excess_return'].rolling(window=window).mean()
rolling_std = df['excess_return'].rolling(window=window).std() # 默认 ddof=1 样本标准差

# 年化滚动夏普比率 = (日超额均值 / 日标准差) * sqrt(252)
df['rolling_sharpe'] = (rolling_mean_excess / rolling_std) * np.sqrt(trading_days)

# ==========================================
# 3. 报告最后一个窗口的值；画出时间序列
# ==========================================
# 提取最后一个有效窗口值
rolling_sharpe_last = df['rolling_sharpe'].dropna().iloc[-1]

# 打印结果供课堂投屏查看
print(f"最后一个{window}日滚动年化夏普比率值: {rolling_sharpe_last:.4f}")

# 绘制时间序列图
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['rolling_sharpe'], label=f'{window}-Day Rolling Annualized Sharpe', color='blue')
plt.axhline(y=0, color='red', linestyle='--', linewidth=1)

plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf={rf_annual*100:.1f}%)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
figure_path = 'rolling_sharpe_plot.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 按输出契约封装结果
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}
