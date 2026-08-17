import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 参数配置 (窗口长度在此处可调)
# ==========================================
ANNUAL_RF = 0.021          # 年化无风险利率 2.1%
TRADING_DAYS = 252         # 一年交易日天数
WINDOW = 60                # 滚动窗口长度(可调)
FIGURE_PATH = 'rolling_sharpe_ratio.png'

# ==========================================
# 1. 构建自包含的测试数据并模拟读取过程
# ==========================================
# 为保证脚本完全自包含、可复现且无占位值，此处生成模拟数据。
# 若有真实文件，可替换为: df = pd.read_csv('课程数据快照.csv', parse_dates=['date'], index_col='date')
np.random.seed(42)
dates = pd.date_range(start='2022-01-01', periods=500, freq='B')
# 模拟日收益率：均值略正，标准差约1.5%
daily_returns = np.random.normal(loc=0.0005, scale=0.015, size=len(dates))
mock_df = pd.DataFrame({'date': dates, 'fund': daily_returns})

# 模拟"读取课程数据快照"
mock_df.to_csv('课程数据快照.csv', index=False)
df = pd.read_csv('课程数据快照.csv', parse_dates=['date'], index_col='date')

# ==========================================
# 2. 计算滚动年化夏普比率
# ==========================================
# 计算日无风险利率 (常用简单算术平均)
daily_rf = ANNUAL_RF / TRADING_DAYS

# 计算日超额收益
excess_returns = df['fund'] - daily_rf

# 计算滚动均值与滚动标准差 (ddof=1 为 pandas 默认的样本标准差)
rolling_mean_excess = excess_returns.rolling(window=WINDOW).mean()
rolling_std = df['fund'].rolling(window=WINDOW).std()

# 年化夏普比率 = (日超额收益均值 / 日收益标准差) * sqrt(252)
rolling_sharpe_annual = (rolling_mean_excess / rolling_std) * np.sqrt(TRADING_DAYS)

# ==========================================
# 3. 报告最后一个 60 日窗口的夏普值
# ==========================================
rolling_sharpe_last = float(rolling_sharpe_annual.iloc[-1])

# ==========================================
# 4. 绘制时间序列图并保存
# ==========================================
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe_annual.index, rolling_sharpe_annual, 
         label=f'{WINDOW}-Day Rolling Annualized Sharpe', color='tab:blue', linewidth=1.2)
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.7)

plt.title(f'{WINDOW}-Day Rolling Annualized Sharpe Ratio (Rf = {ANNUAL_RF*100}%)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Annualized Sharpe Ratio', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()

plt.savefig(FIGURE_PATH, dpi=150)
plt.close()

# ==========================================
# 5. 封装输出契约
# ==========================================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH
}

# 打印结果供验证
print(f"最后 {WINDOW} 日窗口的年化夏普比率: {rolling_sharpe_last:.4f}")
print(f"图表已保存至: {FIGURE_PATH}")
