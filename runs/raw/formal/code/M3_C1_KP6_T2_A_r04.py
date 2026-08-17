import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ============================================================
# 由于未提供实际数据，此处生成示例数据以演示完整流程
# 如有真实数据，请替换 df 的构建部分
# ============================================================
np.random.seed(42)
dates = pd.bdate_range(start='2022-01-01', end='2024-12-31', freq='B')
daily_returns = np.random.normal(0.0004, 0.012, len(dates))
df = pd.DataFrame({'fund': daily_returns}, index=dates)
df.index.name = 'date'

# ============================================================
# 核心计算：滚动年化夏普比率
# ============================================================
def calc_rolling_sharpe(returns, window, rf_annual=0.021):
    """
    计算滚动年化夏普比率
    - returns: 日收益率序列
    - window: 滚动窗口（交易日天数）
    - rf_annual: 年化无风险利率
    """
    rf_daily = (1 + rf_annual) ** (1 / 252) - 1  # 日化无风险利率
    rolling_mean = returns.rolling(window=window).mean()
    rolling_std = returns.rolling(window=window).std()
    rolling_sharpe = (rolling_mean - rf_daily) / rolling_std * np.sqrt(252)
    return rolling_sharpe

# 默认窗口
default_window = 60

# 计算默认窗口下的滚动夏普
rolling_sharpe = calc_rolling_sharpe(df['fund'], default_window, rf_annual=0.021)

# 最后一个窗口的数值
last_value = rolling_sharpe.iloc[-1]

# ============================================================
# 绘图：带可调窗口滑块的曲线
# ============================================================
fig, ax = plt.subplots(figsize=(14, 6))
plt.subplots_adjust(bottom=0.22)

line, = ax.plot(rolling_sharpe.dropna().index, rolling_sharpe.dropna().values,
                color='#1f77b4', linewidth=1.2, label=f'Rolling Sharpe (window={default_window})')
ax.axhline(y=0, color='gray', linestyle='--', linewidth=0.8)
ax.set_title(f'Rolling Annualized Sharpe Ratio (rf=2.1%, window={default_window})', fontsize=14)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Sharpe Ratio', fontsize=12)
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# 添加滑块
ax_slider = plt.axes([0.15, 0.05, 0.7, 0.03])
slider = Slider(ax_slider, 'Window', 10, 120, valinit=default_window, valstep=5)

def update(val):
    window = int(slider.val)
    rs = calc_rolling_sharpe(df['fund'], window, rf_annual=0.021).dropna()
    line.set_data(rs.index, rs.values)
    ax.set_title(f'Rolling Annualized Sharpe Ratio (rf=2.1%, window={window})', fontsize=14)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

slider.on_changed(update)

# 保存图片
figure_path = 'rolling_sharpe.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ============================================================
# 输出契约
# ============================================================
result = {
    'rolling_sharpe_last': round(last_value, 6),
    'figure_path': figure_path
}

print(result)
