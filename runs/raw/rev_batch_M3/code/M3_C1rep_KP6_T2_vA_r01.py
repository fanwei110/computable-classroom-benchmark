import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ================= 1. 数据准备 =================
# 注意：此处生成虚拟数据用于演示。实际使用时，请替换为您的真实数据
# df = pd.read_csv('your_data.csv', parse_dates=['date'], index_col='date')
# 如果 'fund' 列是净值，需先转换为日收益率：df['fund'] = df['fund'].pct_change()

np.random.seed(42)
dates = pd.date_range(start='2021-01-01', periods=500)
# 模拟日收益率数据 (均值为正，符合一般基金特征)
returns = np.random.normal(loc=0.0005, scale=0.015, size=500)
df = pd.DataFrame({'fund': returns}, index=dates)

# ================= 2. 计算滚动夏普函数 =================
def calc_rolling_sharpe(returns, window, rf=0.021):
    """
    计算滚动年化夏普比率
    :param returns: 日收益率序列
    :param window: 滚动窗口大小（交易日）
    :param rf: 年化无风险利率
    """
    # 年化平均收益率
    rolling_mean = returns.rolling(window=window).mean() * 252
    # 年化波动率
    rolling_std = returns.rolling(window=window).std() * np.sqrt(252)
    # 滚动年化夏普
    sharpe = (rolling_mean - rf) / rolling_std
    return sharpe

# ================= 3. 初始计算与获取最后一个值 =================
init_window = 60
rf = 0.021
df['rolling_sharpe'] = calc_rolling_sharpe(df['fund'], init_window, rf)

# 获取最后一个有效（非NaN）的夏普数值
last_sharpe_val = df['rolling_sharpe'].dropna().iloc[-1]

# ================= 4. 绘图与窗口可调 =================
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(bottom=0.2)  # 为底部滑块留出空间

line, = ax.plot(df.index, df['rolling_sharpe'], label=f'Rolling Sharpe (Window={init_window})', color='tab:blue')
ax.axhline(0, color='red', linestyle='--', alpha=0.5)
ax.set_title(f'{init_window}日滚动年化夏普 (rf={rf*100}%)')
ax.set_ylabel('Sharpe Ratio')
ax.legend()
ax.grid(True, alpha=0.3)

# 添加滑块实现窗口可调
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
slider = Slider(ax_slider, 'Window', 10, 120, valinit=init_window, valstep=5)

def update(val):
    w = int(slider.val)
    new_sharpe = calc_rolling_sharpe(df['fund'], w, rf)
    line.set_ydata(new_sharpe)
    ax.set_title(f'{w}日滚动年化夏普 (rf={rf*100}%)')
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

slider.on_changed(update)

# ================= 5. 保存图片与输出契约 =================
fig_path = 'rolling_sharpe_curve.png'
plt.savefig(fig_path)

# 严格按照输出契约组装结果
result = {
    'rolling_sharpe_last': last_sharpe_val,
    'figure_path': fig_path
}

print(result)
