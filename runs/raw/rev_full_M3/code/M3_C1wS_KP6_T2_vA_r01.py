import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==========================================
# 1. 读取快照 CSV；计入无风险利率
# ==========================================
# 假设处理：为保障脚本完全自包含与可复现，若当前目录下没有快照文件，则自动生成确定性的模拟数据
csv_path = 'snapshot.csv'
if not os.path.exists(csv_path):
    np.random.seed(42)  # 确保可复现
    # 生成250个交易日的模拟数据
    dates = pd.date_range(start='2023-01-01', periods=250, freq='B')
    # 模拟日收益率：均值为正，标准差适中
    daily_returns = np.random.normal(loc=0.0008, scale=0.015, size=len(dates))
    # 生成基金净值序列，初始净值为1.0
    nav = 1.0 * (1 + daily_returns).cumprod()
    df_mock = pd.DataFrame({'date': dates, 'fund': nav})
    df_mock.to_csv(csv_path, index=False)

# 读取数据
df = pd.read_csv(csv_path)

# 假设处理：若存在日期列则解析并排序，否则按行号排序
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    has_date = True
else:
    has_date = False

# 前向填充处理可能的缺失值
df['fund'] = df['fund'].ffill()

# 计算日收益率
df['daily_return'] = df['fund'].pct_change()

# ==========================================
# 2. 计算 60 日滚动年化夏普，窗口可调
# ==========================================
# 假设处理：
# - 一年按252个交易日计算年化因子
# - 日无风险利率 = 年化无风险利率 / 252
# - 样本标准差自由度 ddof=1 (pandas默认)
rf_annual = 0.021
trading_days = 252
rf_daily = rf_annual / trading_days
window = 60  # 窗口大小，可在此处调整

# 计算滚动均值与滚动标准差
rolling_mean = df['daily_return'].rolling(window=window).mean()
rolling_std = df['daily_return'].rolling(window=window).std()

# 计算滚动年化夏普比率：[(日均值 - 日无风险利率) / 日标准差] * sqrt(252)
rolling_sharpe_annual = ((rolling_mean - rf_daily) / rolling_std) * np.sqrt(trading_days)

# ==========================================
# 3. 报告最后一个窗口的值；画出时间序列
# ==========================================
# 提取最后一个有效窗口的数值，转换为原生float
rolling_sharpe_last = float(rolling_sharpe_annual.iloc[-1])

# 绘制时间序列图
plt.figure(figsize=(12, 6))
valid_idx = rolling_sharpe_annual.notna()

if has_date:
    plt.plot(df.loc[valid_idx, 'date'], rolling_sharpe_annual[valid_idx], 
             label=f'{window}-Day Rolling Annualized Sharpe', color='royalblue', linewidth=1.5)
    plt.xlabel('Date', fontsize=12)
else:
    plt.plot(rolling_sharpe_annual[valid_idx].index, rolling_sharpe_annual[valid_idx], 
             label=f'{window}-Day Rolling Annualized Sharpe', color='royalblue', linewidth=1.5)
    plt.xlabel('Trading Days', fontsize=12)

plt.axhline(0, color='red', linestyle='--', linewidth=0.8, alpha=0.7)
plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf={rf_annual*100}%)', fontsize=14)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
fig_path = 'rolling_sharpe_curve.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')
plt.close()

# 按照输出契约构造字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': fig_path
}

# 课堂打印输出，便于投屏确认
print(f"最后一个窗口({window}日)的滚动年化夏普数值: {rolling_sharpe_last:.4f}")
print(f"图形已保存至: {fig_path}")
print("Result Dictionary:", result)
