import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ================= 1. 数据准备 =================
# 假设 df 为包含 'fund' 列的日收益率数据（若为净值，需先 .pct_change() 计算）
# 这里生成模拟数据以供演示
np.random.seed(2023)
dates = pd.date_range(start='2022-01-01', periods=500, freq='B')
fund_returns = np.random.normal(0.0005, 0.02, size=len(dates))
df = pd.DataFrame({'fund': fund_returns}, index=dates)

# ================= 2. 参数设置 =================
rf = 0.021         # 无风险利率（小数表示）
trading_days = 252  # 一年252个交易日
init_window = 60   # 初始滚动窗口

# ================= 3. 计算逻辑 =================
# 按年复利报价将年化无风险利率转换为日化无风险利率
rf_daily = (1 + rf) ** (1 / trading_days) - 1

# 计算日超额收益
excess_returns = df['fund'] - rf_daily

def calc_rolling_sharpe(excess_returns, window):
    # 标准差用样本估计量（ddof=1）
    rolling_std = excess_returns.rolling(window=window).std(ddof=1)
    rolling_mean = excess_returns.rolling(window=window).mean()
    # 年化夏普 = (均值/标准差) * sqrt(252)
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(trading_days)
    return rolling_sharpe

# 计算初始滚动夏普并提取最后一个有效窗口的数值
rolling_sharpe_init = calc_rolling_sharpe(excess_returns, init_window)
last_sharpe_value = rolling_sharpe_init.dropna().iloc[-1]

# ================= 4. 绘图与交互 =================
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)

# 初始曲线
line, = ax.plot(rolling_sharpe_init.dropna(), color='darkblue', linewidth=1.2)
ax.set_title(f'Rolling {init_window}-Day Annualized Sharpe Ratio (rf={rf*100}%)')
ax.set_xlabel('Date')
ax.set_ylabel('Sharpe Ratio')
ax.grid(True, linestyle='--', alpha=0.6)

# 增加滑块组件实现窗口可调
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
slider = Slider(ax_slider, 'Window', 10, 252, valinit=init_window, valstep=1)

def update(val):
    window = int(slider.val)
    y = calc_rolling_sharpe(excess_returns, window).dropna()
    line.set_xdata(y.index)
    line.set_ydata(y)
    ax.set_title(f'Rolling {window}-Day Annualized Sharpe Ratio (rf={rf*100}%)')
    ax.relim()
    ax.autoscale_view()
    plt.draw()

slider.on_changed(update)

# ================= 5. 保存图片与输出结果 =================
fig_path = 'rolling_sharpe_curve.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')

# 按照输出契约存入 result 字典
result = {
    'rolling_sharpe_last': last_sharpe_value,
    'figure_path': fig_path
}

# 打印验证
print(f"最后那个窗口的数值: {last_sharpe_value:.4f}")
print(f"result字典: {result}")
