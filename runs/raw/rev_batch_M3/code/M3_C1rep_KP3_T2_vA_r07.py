import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import json

# 设置中文字体与负号显示
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 债券参数
F = 100
coupon_rate = 0.046
T = 7
y0 = 0.053
C = F * coupon_rate

# 精确价格计算函数
def bond_price(y):
    price = 0
    for t in range(1, T + 1):
        price += C / (1 + y)**t
    price += F / (1 + y)**T
    return price

P0 = bond_price(y0)

# 久期计算函数
def mac_duration(y, P):
    dur = 0
    for t in range(1, T + 1):
        dur += t * (C / (1 + y)**t)
    dur += T * (F / (1 + y)**T)
    return dur / P

mac_dur = mac_duration(y0, P0)
mod_dur = mac_dur / (1 + y0)

# 久期近似价格函数（切线）
def approx_price(y):
    return P0 * (1 - mod_dur * (y - y0))

# 生成收益率与价格数据
y_vals = np.linspace(0.02, 0.09, 1000)
exact_prices = np.array([bond_price(y) for y in y_vals])
approx_prices = np.array([approx_price(y) for y in y_vals])

# 计算上升100个基点后的结果
delta_y = 0.01
y_up = y0 + delta_y
price_at_up100bp = bond_price(y_up)
dur_approx_change_up100bp = -mod_dur * delta_y

# 构建 result 字典
result = {
    'price_at_up100bp': round(price_at_up100bp, 4),
    'dur_approx_change_up100bp': round(dur_approx_change_up100bp, 6),
    'figure_path': 'bond_price_yield_curve.png'
}

# ---------- 绘图部分 ----------
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

# 绘制曲线
ax.plot(y_vals * 100, exact_prices, label='精确价格', color='blue', linewidth=2)
ax.plot(y_vals * 100, approx_prices, label='久期近似价格', color='red', linestyle='--', linewidth=2)

# 标记初始点和100bp变动点
point_exact, = ax.plot((y0 + delta_y) * 100, price_at_up100bp, 'bo', markersize=8)
point_approx, = ax.plot((y0 + delta_y) * 100, approx_price(y0 + delta_y), 'ro', markersize=8)
line_delta, = ax.plot([y0*100, (y0+delta_y)*100], [P0, approx_price(y0 + delta_y)], 'k--', alpha=0.5)

ax.set_xlabel('收益率 (%)')
ax.set_ylabel('价格')
ax.set_title('债券价格随收益率变化曲线及久期近似')
ax.legend()
ax.grid(True)

# 添加收益率变动幅度可调滑块 (范围为 -3.3% 到 +3.7%，保证收益率在 2%~9% 内)
ax_delta = plt.axes([0.2, 0.1, 0.6, 0.03])
slider_delta = Slider(ax_delta, '收益率变动(%)', -3.3, 3.7, valinit=1.0, valstep=0.1)

def update(val):
    dy = slider_delta.val / 100.0
    y_new = y0 + dy
    p_exact = bond_price(y_new)
    p_approx = approx_price(y_new)
    point_exact.set_ydata([p_exact])
    point_exact.set_xdata([y_new * 100])
    point_approx.set_ydata([p_approx])
    point_approx.set_xdata([y_new * 100])
    line_delta.set_xdata([y0 * 100, y_new * 100])
    line_delta.set_ydata([P0, p_approx])
    fig.canvas.draw_idle()

slider_delta.on_changed(update)

# 保存图表
plt.savefig(result['figure_path'], dpi=300, bbox_inches='tight')
plt.close()

# 保存结果字典至本地
with open('result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print(result)
