import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ================= 参数设置 =================
# 窗口长度设为可调变量，可随时修改
WINDOW_SIZE = 60
# 年化无风险利率
RF_ANNUAL = 0.021
# 一年交易日天数（金融计算常规假设）
TRADING_DAYS_PER_YEAR = 252
# 文件路径
DATA_PATH = 'data/market_snapshot_v1.csv'
FIGURE_PATH = 'rolling_sharpe_ratio.png'

# ================= 步骤 1: 读取数据并计入无风险利率 =================
# 读取课程数据快照
df = pd.read_csv(DATA_PATH)
# 提取 'fund' 列的日收益率
daily_returns = df['fund']

# 计算日无风险利率 (采用单利近似，与业界日度超额收益计算惯例一致)
rf_daily = RF_ANNUAL / TRADING_DAYS_PER_YEAR

# 计算日超额收益
daily_excess_returns = daily_returns - rf_daily

# ================= 步骤 2: 计算滚动年化夏普比率 =================
# 计算滚动均值和滚动标准差 (pandas默认 ddof=1 为样本标准差，符合统计惯例)
rolling_mean = daily_excess_returns.rolling(window=WINDOW_SIZE).mean()
rolling_std = daily_excess_returns.rolling(window=WINDOW_SIZE).std()

# 计算日度夏普比率并年化：年化夏普 = 日夏普 * sqrt(252)
rolling_sharpe_daily = rolling_mean / rolling_std
rolling_sharpe_annualized = rolling_sharpe_daily * np.sqrt(TRADING_DAYS_PER_YEAR)

# ================= 步骤 3: 报告最后一个窗口值并画图 =================
# 获取最近一个窗口的夏普值，转为Python原生float
rolling_sharpe_last = float(rolling_sharpe_annualized.iloc[-1])

# 绘制时间序列图
plt.figure(figsize=(12, 6))
plt.plot(rolling_sharpe_annualized, color='tab:blue', linewidth=1.5, 
         label=f'{WINDOW_SIZE}-Day Rolling Annualized Sharpe Ratio')

# 添加标题和标签 (采用英文标注以避免不同操作系统环境下中文字体缺失导致的乱码，保证课堂投屏效果)
plt.title(f'{WINDOW_SIZE}-Day Rolling Annualized Sharpe Ratio (Rf = {RF_ANNUAL*100:.1f}%)', fontsize=16)
plt.xlabel('Trading Days', fontsize=13)
plt.ylabel('Annualized Sharpe Ratio', fontsize=13)
plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()

# ================= 步骤 4: 保存图形并填充 result =================
plt.savefig(FIGURE_PATH, dpi=150)
plt.close()

# 按照输出契约构建结果字典
result = {
    'rolling_sharpe_last': rolling_sharpe_last,
    'figure_path': FIGURE_PATH
}

# 控制台输出结果，便于课堂展示与验证
print(f"Last {WINDOW_SIZE}-day window annualized Sharpe ratio: {rolling_sharpe_last:.4f}")
print(f"Figure saved to: {FIGURE_PATH}")
print(f"Result dictionary: {result}")
