import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# 0. 生成模拟快照CSV (保证脚本完全自包含)
# ==========================================
csv_path = 'fund_snapshot.csv'
if not os.path.exists(csv_path):
    np.random.seed(42)
    # 生成约1.5年的交易日数据
    dates = pd.date_range(start='2023-01-01', periods=300, freq='B')
    # 模拟日频基金收益率 (均值为正，标准差约为1.5%)
    fund_returns = np.random.normal(loc=0.0005, scale=0.015, size=300)
    df_mock = pd.DataFrame({'date': dates, 'fund': fund_returns})
    df_mock.to_csv(csv_path, index=False)

# ==========================================
# 1. 读取快照 CSV；计入无风险利率
# ==========================================
# 假设 CSV 包含 'date' 和 'fund' 列，'fund' 为日频收益率(小数形式)
df = pd.read_csv(csv_path, parse_dates=['date'])
df.sort_values('date', inplace=True)
df.reset_index(drop=True, inplace=True)

# 无风险利率与周期假设
rf_annual = 0.021          # 年化无风险利率 2.1%
trading_days = 252         # 假设一年252个交易日
rf_daily = rf_annual / trading_days  # 日化无风险利率

# 计算日超额收益
df['excess_return'] = df['fund'] - rf_daily

# ==========================================
# 2. 计算 60 日滚动年化夏普，窗口可调
# ==========================================
window = 60  # 滚动窗口大小（可在此调整）

# 计算滚动均值与标准差
rolling_mean = df['excess_return'].rolling(window=window).mean()
rolling_std = df['excess_return'].rolling(window=window).std()

# 年化夏普比率 = (日夏普比率) * sqrt(252)
# 日夏普比率 = 滚动超额收益均值 / 滚动超额收益标准差
df['rolling_sharpe_annualized'] = (rolling_mean / rolling_std) * np.sqrt(trading_days)

# ==========================================
# 3. 报告最后一个窗口的值；画出时间序列
# ==========================================
# 提取最后一个非NaN的滚动夏普值
rolling_sharpe_last = df['rolling_sharpe_annualized'].dropna().iloc[-1]

# 绘制时间序列图
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(df['date'], df['rolling_sharpe_annualized'], 
        label=f'{window}-Day Rolling Annualized Sharpe', 
        color='tab:blue', linewidth=1.5)

# 添加零线与格式修饰
ax.axhline(0, color='red', linestyle='--', linewidth=0.8, alpha=0.7)
ax.set_title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf={rf_annual:.1%})', fontsize=14)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend(fontsize=11)

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
figure_path = 'rolling_sharpe_ratio.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# 严格遵循输出契约
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

# 课堂演示输出
print(f"最后一个窗口的年化夏普比率: {result['rolling_sharpe_last']:.4f}")
print(f"图形已保存至: {result['figure_path']}")
