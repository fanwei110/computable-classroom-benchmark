import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# ============================================================
# 1. 读取快照 CSV；计入无风险利率
# ============================================================
# 假设 CSV 文件名为 'snapshot.csv'，包含至少 'date' 和 'fund' 两列
# 如果文件不存在，创建一个模拟数据用于演示
csv_file = 'snapshot.csv'

if not os.path.exists(csv_file):
    # 生成模拟数据：252个交易日，约一年
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', periods=252, freq='B')
    returns = np.random.normal(0.0005, 0.015, 252)  # 日收益率均值0.05%，标准差1.5%
    df = pd.DataFrame({'date': dates, 'fund': returns})
    df.to_csv(csv_file, index=False)
    print("已创建模拟数据文件 snapshot.csv")
else:
    df = pd.read_csv(csv_file, parse_dates=['date'])

# 确保按日期排序
df = df.sort_values('date').reset_index(drop=True)

# 无风险利率（年化）
rf_annual = 0.021  # 2.1%
# 转换为日度无风险利率（假设252个交易日）
rf_daily = (1 + rf_annual) ** (1/252) - 1

# ============================================================
# 2. 计算 60 日滚动年化夏普，窗口可调
# ============================================================
window = 60  # 滚动窗口大小（可调整）

# 超额收益：基金日收益率 - 无风险日利率
df['excess_return'] = df['fund'] - rf_daily

# 滚动计算：窗口内超额收益的年化夏普比率
# 年化夏普 = (日超额收益均值 / 日超额收益标准差) * sqrt(252)
rolling_sharpe = []
for i in range(len(df)):
    if i < window - 1:
        rolling_sharpe.append(np.nan)
    else:
        window_data = df['excess_return'].iloc[i - window + 1 : i + 1]
        mean_excess = window_data.mean()
        std_excess = window_data.std()
        if std_excess == 0 or np.isnan(std_excess):
            sharpe = np.nan
        else:
            sharpe_daily = mean_excess / std_excess
            sharpe_annual = sharpe_daily * np.sqrt(252)
        rolling_sharpe.append(sharpe_annual)

df['rolling_sharpe'] = rolling_sharpe

# ============================================================
# 3. 报告最后一个窗口的值
# ============================================================
rolling_sharpe_last = df['rolling_sharpe'].iloc[-1]
print(f"最后一个 {window} 日滚动年化夏普比率: {rolling_sharpe_last:.4f}")

# ============================================================
# 4. 画出时间序列并保存图形
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df['date'], df['rolling_sharpe'], 
        linewidth=1.5, color='steelblue', label=f'{window}-Day Rolling Sharpe Ratio')

ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
ax.axhline(y=rolling_sharpe_last, color='red', linestyle='--', linewidth=1.0, 
           alpha=0.7, label=f'Last Value: {rolling_sharpe_last:.4f}')

ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
ax.set_title(f'{window}-Day Rolling Annualized Sharpe Ratio (Risk-Free Rate: {rf_annual*100:.1f}%)', 
             fontsize=14, fontweight='bold')
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图形
figure_path = 'rolling_sharpe_ratio.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
print(f"图形已保存至: {figure_path}")

# ============================================================
# 输出契约：将所有要求输出存入 result 字典
# ============================================================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

# 打印结果以便验证
print("\n=== 输出结果 ===")
print(f"rolling_sharpe_last: {result['rolling_sharpe_last']:.6f}")
print(f"figure_path: {result['figure_path']}")

plt.show()
