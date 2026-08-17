import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. 读取快照 CSV；计入无风险利率
# ==========================================
# 为保证脚本自包含且可复现，若当前目录下不存在快照文件，则生成模拟数据
csv_path = 'snapshot.csv'

if not os.path.exists(csv_path):
    np.random.seed(42)
    # 模拟250个交易日的数据
    dates = pd.date_range(start='2023-01-01', periods=250, freq='B')
    # 模拟基金净值：初始净值1.0，带有微弱的向上漂移和波动
    daily_returns = np.random.normal(loc=0.0005, scale=0.015, size=len(dates))
    fund_nav = 1.0 * np.cumprod(1 + daily_returns)
    df_mock = pd.DataFrame({'date': dates, 'fund': fund_nav})
    df_mock.to_csv(csv_path, index=False)

# 读取数据
df = pd.read_csv(csv_path)

# 假设日期列名为 'date'，若不存在则按顺序生成索引
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
else:
    df.index = pd.date_range(start='2023-01-01', periods=len(df), freq='B')

# ==========================================
# 2. 计算 60 日滚动年化夏普，窗口可调
# ==========================================
# 参数设置
rf_annual = 0.021          # 年化无风险利率 2.1%
trading_days = 252         # 一年交易日假设
rf_daily = rf_annual / trading_days  # 日无风险利率
window = 60                # 滚动窗口大小（可调）

# 假设 fund 列为基金净值序列，计算日收益率
df['daily_return'] = df['fund'].pct_change()

# 计算超额收益
df['excess_return'] = df['daily_return'] - rf_daily

# 计算滚动均值与滚动标准差
rolling_mean_excess = df['excess_return'].rolling(window=window).mean()
rolling_std = df['daily_return'].rolling(window=window).std()

# 计算滚动年化夏普比率
# 年化夏普 = (日均超额收益 / 日收益标准差) * sqrt(252)
df['rolling_sharpe_annualized'] = (rolling_mean_excess / rolling_std) * np.sqrt(trading_days)

# ==========================================
# 3. 报告最后一个窗口的值；画出时间序列
# ==========================================
# 获取最后一个有效窗口的值
rolling_sharpe_last = df['rolling_sharpe_annualized'].iloc[-1]

# 绘制时间序列图
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['rolling_sharpe_annualized'], 
         label=f'{window}-Day Rolling Annualized Sharpe', 
         color='tab:blue', linewidth=1.5)

# 添加零线参考
plt.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.7)

# 标注最后一个点的数值
last_date = df.index[-1]
plt.scatter(last_date, rolling_sharpe_last, color='black', zorder=5)
plt.annotate(f'{rolling_sharpe_last:.4f}', 
             xy=(last_date, rolling_sharpe_last), 
             xytext=(-50, 20), 
             textcoords='offset points',
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
             fontsize=11, fontweight='bold',
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1))

plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf={rf_annual*100}%)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
figure_path = 'rolling_sharpe_60d.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 按照输出契约存入字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

# 打印结果供课堂投屏验证
print(f"最后一个窗口的滚动年化夏普比率为: {rolling_sharpe_last:.4f}")
print(f"图形已保存至: {figure_path}")
print(result)
