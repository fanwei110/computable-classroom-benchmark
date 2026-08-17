import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ==========================================
# 0. 自包含数据准备（模拟快照CSV以保障可复现运行）
# ==========================================
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', periods=200, freq='B')
fund_returns = np.random.normal(loc=0.0005, scale=0.02, size=200)
df_mock = pd.DataFrame({'date': dates, 'fund': fund_returns})
csv_path = 'snapshot.csv'
df_mock.to_csv(csv_path, index=False)

# ==========================================
# 1. 读取快照 CSV；计入无风险利率
# ==========================================
df = pd.read_csv(csv_path)

# 假设与参数设置
rf_annual = 0.021          # 题目给定年化无风险利率 2.1%
trading_days = 252         # 假设一年252个交易日
rf_daily = rf_annual / trading_days  # 假设计算日超额收益采用简单算术平均折算日无风险利率

# ==========================================
# 2. 计算 60 日滚动年化夏普，窗口可调
# ==========================================
window = 60  # 滚动窗口大小，可按需调整

# 计算日超额收益
excess_returns = df['fund'] - rf_daily

# 计算滚动均值与滚动标准差
rolling_mean = excess_returns.rolling(window=window).mean()
rolling_std = excess_returns.rolling(window=window).std()

# 计算滚动年化夏普比率 (日夏普 * sqrt(252))
rolling_sharpe_annualized = (rolling_mean / rolling_std) * np.sqrt(trading_days)

# ==========================================
# 3. 报告最后一个窗口的值；画出时间序列
# ==========================================
# 剔除前期NaN，获取有效滚动夏普值
valid_sharpe = rolling_sharpe_annualized.dropna()

# 获取最后一个窗口的值
rolling_sharpe_last = valid_sharpe.iloc[-1]

# 绘制时间序列图
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(valid_sharpe.index, valid_sharpe.values, label=f'{window}-Day Rolling Sharpe Ratio', color='royalblue', linewidth=1.5)
ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
ax.set_title(f'{window}-Day Rolling Annualized Sharpe Ratio (rf={rf_annual*100}%)', fontsize=14)
ax.set_xlabel('Trading Days Index', fontsize=12)
ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
ax.legend(fontsize=11)
ax.grid(True, linestyle='--', alpha=0.6)

# ==========================================
# 4. 保存图形并填充 result
# ==========================================
figure_path = 'rolling_sharpe.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 按输出契约存入字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

# 课堂展示辅助打印
print(f"最后一个窗口({window}日)的滚动年化夏普比率: {rolling_sharpe_last:.4f}")
print(f"图形已保存至: {figure_path}")
print("Result Dictionary:", result)
