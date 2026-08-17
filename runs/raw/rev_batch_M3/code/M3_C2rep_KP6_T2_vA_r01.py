import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数与假设 ====================
# 题目未指明的计算选择作如下内部一致的假设：
# 1. 一年交易日天数：252天（国际及国内主流惯例）
# 2. 日无风险利率换算：采用简单除法 rf_daily = rf_annual / 252
# 3. 滚动标准差：采用样本标准差 (ddof=1)，即 pandas 默认的滚动标准差计算方式
# 4. 年化夏普比率 = 日夏普比率 * sqrt(252)

ANNUAL_RISK_FREE_RATE = 0.021
TRADING_DAYS_PER_YEAR = 252
ROLLING_WINDOW = 60  # 窗口长度可调：修改此变量即可调整滚动窗口

# ==================== 1. 读取快照 CSV；计入无风险利率 ====================
# 读取数据
df = pd.read_csv('data/market_snapshot_v1.csv')

# 计算日无风险利率
rf_daily = ANNUAL_RISK_FREE_RATE / TRADING_DAYS_PER_YEAR

# 提取基金日收益率并计算日超额收益
daily_returns = df['fund']
excess_returns = daily_returns - rf_daily

# ==================== 2. 计算 60 日滚动年化夏普，窗口可调 ====================
# 计算滚动均值与滚动标准差
rolling_mean = excess_returns.rolling(window=ROLLING_WINDOW).mean()
rolling_std = excess_returns.rolling(window=ROLLING_WINDOW).std()

# 计算滚动年化夏普比率
rolling_sharpe_annualized = (rolling_mean / rolling_std) * np.sqrt(TRADING_DAYS_PER_YEAR)

# ==================== 3. 报告最后一个窗口的值；画出时间序列 ====================
# 提取最后一个窗口的夏普值
last_sharpe_value = rolling_sharpe_annualized.iloc[-1]

# 打印最后一个窗口的夏普值
print(f"最后 {ROLLING_WINDOW} 日滚动年化夏普比率: {last_sharpe_value:.4f}")

# 绘制时间序列图
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe_annualized, label=f'Rolling Annualized Sharpe (Window={ROLLING_WINDOW})', color='#1f77b4')
plt.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.8)
plt.title(f'{ROLLING_WINDOW}-Day Rolling Annualized Sharpe Ratio (Rf={ANNUAL_RISK_FREE_RATE*100:.1f}%)')
plt.xlabel('Time (Index)')
plt.ylabel('Annualized Sharpe Ratio')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()

# ==================== 4. 保存图形并填充 result ====================
# 保存图形
figure_path = 'rolling_sharpe_ratio.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# 填充结果字典
result = {
    'rolling_sharpe_last': float(last_sharpe_value) if not pd.isna(last_sharpe_value) else None,
    'figure_path': figure_path
}
