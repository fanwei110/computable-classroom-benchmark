import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========================
# 1. 读取数据与参数设定
# ========================
# 读取课程数据快照
df = pd.read_csv('data/market_snapshot_v1.csv')
fund_return = df['fund']

# 课程约定参数
rf_annual = 0.021              # 年化无风险利率 2.1%
rf_daily = rf_annual / 252     # 日无风险利率
window = 60                    # 滚动窗口长度，可按需调整

# ========================
# 2. 计算滚动年化夏普比率
# ========================
# 计算日超额收益
excess_return = fund_return - rf_daily

# 计算滚动均值与滚动标准差（ddof=1 为样本标准差）
rolling_mean = excess_return.rolling(window=window).mean()
rolling_std = excess_return.rolling(window=window).std(ddof=1)

# 计算滚动年化夏普比率：(均值 / 标准差) * sqrt(252)
rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)

# ========================
# 3. 报告最后一个窗口的值
# ========================
# 提取最近一个完整窗口的夏普比率值
rolling_sharpe_last = rolling_sharpe.dropna().iloc[-1]

# ========================
# 4. 绘制时间序列图并保存
# ========================
# 设置 matplotlib 显示参数（防备中文及负号显示异常）
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))
rolling_sharpe.plot(ax=ax, color='blue', linewidth=1.2)

ax.set_title(f'{window}-Day Rolling Annualized Sharpe Ratio', fontsize=14)
ax.set_xlabel('Trading Day', fontsize=12)
ax.set_ylabel('Annualized Sharpe Ratio', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)

# 保存图形
figure_path = 'rolling_sharpe.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ========================
# 5. 填充输出契约字典
# ========================
result = {
    'rolling_sharpe_last': float(rolling_sharpe_last),
    'figure_path': figure_path
}
