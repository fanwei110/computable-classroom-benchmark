import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==================== 参数设置 ====================
rf_annual = 0.021                  # 年化无风险利率 (小数表示)
trading_days = 252                 # 每年交易日数
window = 60                        # 滚动窗口长度，可在此调整
figure_path = 'rolling_sharpe.png' # 图形保存路径

# ==================== 数据读取与预处理 ====================
# 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')

# 提取 'fund' 列的日收益率
fund_returns = df['fund']

# 计算日无风险利率（简单除法）
rf_daily = rf_annual / trading_days

# ==================== 滚动年化夏普比率计算 ====================
# 计算滚动均值
rolling_mean = fund_returns.rolling(window=window).mean()

# 计算滚动标准差（使用样本估计量 ddof=1）
rolling_std = fund_returns.rolling(window=window).std(ddof=1)

# 计算滚动年化夏普比率
# 公式: (滚动均值 - 日无风险利率) / 滚动标准差 * sqrt(252)
rolling_sharpe = (rolling_mean - rf_daily) / rolling_std * np.sqrt(trading_days)

# 提取最后一个窗口的夏普值
rolling_sharpe_last = rolling_sharpe.iloc[-1]

# ==================== 绘图与保存 ====================
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe, label=f'{window}-Day Rolling Sharpe Ratio', color='blue')
plt.title(f'{window}-Day Rolling Annualized Sharpe Ratio (Rf={rf_annual:.1%})', fontsize=14)
plt.xlabel('Date / Index', fontsize=12)
plt.ylabel('Sharpe Ratio', fontsize=12)
plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=12)
plt.tight_layout()

# 保存图形
plt.savefig(figure_path, dpi=150)
plt.close()

# ==================== 输出结果 ====================
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': figure_path
}

# 打印结果供课堂投屏参考
print(f"最后一个 {window} 日窗口的年化夏普比率: {rolling_sharpe_last:.4f}")
print(f"图形已保存至: {figure_path}")
