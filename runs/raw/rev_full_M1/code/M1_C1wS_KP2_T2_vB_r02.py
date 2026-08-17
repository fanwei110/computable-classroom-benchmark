import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 参数设置
initial_rf = 0.023  # 无风险利率 2.3%
initial_market_return = 0.094  # 市场收益率 9.4%

# 股票数据
stocks = {
    'X': {'beta': 0.62, 'return': 0.081},
    'Y': {'beta': 1.18, 'return': 0.131},
    'Z': {'beta': 1.51, 'return': 0.099}
}

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

# 绘制初始SML线
beta_range = np.linspace(0, 2, 100)
sml_line, = ax.plot(beta_range, initial_rf + beta_range * (initial_market_return - initial_rf),
                    'b-', linewidth=2, label='Security Market Line')

# 绘制股票点
for stock, data in stocks.items():
    ax.scatter(data['beta'], data['return'], s=100, label=f'Stock {stock}')
    ax.annotate(stock, (data['beta'], data['return']), textcoords="offset points", xytext=(10,5), ha='center')

# 设置图形属性
ax.set_xlim(0, 2)
ax.set_ylim(0, 0.15)
ax.set_xlabel('Beta')
ax.set_ylabel('Expected Return')
ax.set_title('Security Market Line (SML) with Stocks')
ax.legend()
ax.grid(True)

# 创建滑块
axcolor = 'lightgoldenrodyellow'
ax_rf = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_market = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor=axcolor)

slider_rf = Slider(ax_rf, 'Risk-free Rate', 0.0, 0.1, valinit=initial_rf)
slider_market = Slider(ax_market, 'Market Return', 0.0, 0.2, valinit=initial_market_return)

# 更新函数
def update(val):
    rf = slider_rf.val
    market_return = slider_market.val
    sml_line.set_ydata(rf + beta_range * (market_return - rf))
    fig.canvas.draw_idle()

    # 更新结果
    result['sml_slope'] = market_return - rf
    result['er_at_beta_127'] = rf + 1.27 * (market_return - rf)

slider_rf.on_changed(update)
slider_market.on_changed(update)

# 初始计算结果
result = {
    'sml_slope': initial_market_return - initial_rf,
    'er_at_beta_127': initial_rf + 1.27 * (initial_market_return - initial_rf),
    'figure_path': 'sml_plot.png'
}

# 保存图形
plt.savefig(result['figure_path'])
plt.close()

# 输出结果
print(result)
