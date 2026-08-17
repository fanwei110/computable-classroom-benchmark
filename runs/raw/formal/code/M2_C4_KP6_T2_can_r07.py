import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import os

# ============================================================
# 1. 读取数据并准备
# ============================================================
# 读取CSV文件
data_path = 'data/market_snapshot_v1.csv'
df = pd.read_csv(data_path)

# 提取fund列的日收益率（假设已经是小数形式）
fund_returns = df['fund'].values

# 年化无风险利率
rf_annual = 0.021  # 2.1%
rf_daily = rf_annual / 252  # 日化无风险利率

# ============================================================
# 2. 计算60日滚动年化夏普比率
# ============================================================
window = 60  # 可调窗口长度
n_days = len(fund_returns)

# 初始化滚动夏普比率数组
rolling_sharpe = np.full(n_days, np.nan)

# 逐窗口计算
for i in range(window - 1, n_days):
    # 提取当前窗口的收益率
    window_returns = fund_returns[i - window + 1: i + 1]
    
    # 计算超额收益（减去日无风险利率）
    excess_returns = window_returns - rf_daily
    
    # 计算年化超额收益（日平均超额收益 * 252）
    annualized_excess_return = np.mean(excess_returns) * 252
    
    # 计算年化波动率（日波动率 * sqrt(252)，使用ddof=1）
    annualized_volatility = np.std(window_returns, ddof=1) * np.sqrt(252)
    
    # 计算年化夏普比率
    if annualized_volatility > 0:
        rolling_sharpe[i] = annualized_excess_return / annualized_volatility
    else:
        rolling_sharpe[i] = np.nan

# ============================================================
# 3. 报告最后一个窗口的值
# ============================================================
rolling_sharpe_last = rolling_sharpe[-1]

print(f"最后一个60日窗口的年化夏普比率: {rolling_sharpe_last:.4f}")

# ============================================================
# 4. 绘制时间序列图
# ============================================================
fig, ax = plt.subplots(figsize=(12, 6))

# 只绘制有效数据点（从window-1开始）
valid_indices = np.arange(window - 1, n_days)
valid_sharpe = rolling_sharpe[window - 1:]

ax.plot(valid_indices, valid_sharpe, linewidth=1.5, color='blue', label='60-day Rolling Sharpe Ratio')

# 添加零线参考
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)

# 标注最后一个值
ax.scatter(n_days - 1, rolling_sharpe_last, color='red', s=50, zorder=5,
           label=f'Last Value: {rolling_sharpe_last:.4f}')

# 设置标题和标签
ax.set_title(f'{window}-Day Rolling Annualized Sharpe Ratio', fontsize=14, fontweight='bold')
ax.set_xlabel('Trading Day Index')
ax.set_ylabel('Annualized Sharpe Ratio')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()

# 保存图形
figure_path = 'rolling_sharpe_ratio.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

print(f"图形已保存至: {figure_path}")

# ============================================================
# 5. 构建结果字典
# ============================================================
result = {
    'rolling_sharpe_last': round(rolling_sharpe_last, 6),
    'figure_path': os.path.abspath(figure_path)
}

# 验证结果
print("\n=== 最终结果 ===")
print(f"result['rolling_sharpe_last']: {result['rolling_sharpe_last']:.6f}")
print(f"result['figure_path']: {result['figure_path']}")
