import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数配置 ====================
csv_path = 'data/market_snapshot_v1.csv'
rf_annual = 0.021          # 年化无风险利率 2.1%
window = 60                # 滚动窗口长度，可在此处调整为任意整数
trading_days = 252         # 一年交易日的假设天数，用于年化
figure_path = 'rolling_sharpe_ratio.png'

# ==================== 1. 读取快照CSV ====================
df = pd.read_csv(csv_path)

# 智能识别时间列并将其设为索引，以便绘图时横轴显示为日期
for col in df.columns:
    if 'date' in col.lower() or 'time' in col.lower():
        try:
            df[col] = pd.to_datetime(df[col])
            df.set_index(col, inplace=True)
        except Exception:
            pass
        break

# ==================== 2. 计算滚动年化夏普比率 ====================
# 假设：日度无风险利率 = 年度无风险利率 / 252
rf_daily = rf_annual / trading_days

# 计算超额收益
excess_returns = df['fund'] - rf_daily

# 计算滚动均值和滚动标准差（pandas默认ddof=1，为样本标准差，符合业界惯例）
rolling_mean = excess_returns.rolling(window=window).mean()
rolling_std = excess_returns.rolling(window=window).std()

# 计算滚动年化夏普比率：(均值 / 标准差) * sqrt(252)
rolling_sharpe_annual = (rolling_mean / rolling_std) * np.sqrt(trading_days)

# ==================== 3. 报告最后一个窗口的值并画图 ====================
# 剔除初期因窗口不足产生的NaN，获取有效序列
rolling_sharpe_valid = rolling_sharpe_annual.dropna()

# 提取最近一个窗口的夏普比率
rolling_sharpe_last = rolling_sharpe_valid.iloc[-1]

# 绘制时间序列图
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(rolling_sharpe_valid.index, rolling_sharpe_valid.values, 
        label=f'{window}-Day Rolling Annualized Sharpe', color='royalblue', linewidth=1.5)

ax.set_title(f'{window}-Day Rolling Annualized Sharpe Ratio (Rf={rf_annual*100:.1f}%)', fontsize=14)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.7)
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(fontsize=12)
plt.tight_layout()

# ==================== 4. 保存图形并填充结果字典 ====================
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# 按照输出契约存入字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

# 终端输出验证
print(f"最近一个 {window} 日窗口的年化夏普比率: {rolling_sharpe_last:.4f}")
print(f"图形已保存至: {figure_path}")
