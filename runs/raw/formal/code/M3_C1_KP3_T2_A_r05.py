import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 设置中文字体和负号显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 债券参数
F = 100           # 面值
c = 0.046         # 票息率 4.6%
T = 7             # 期限 7年
y0 = 0.053        # 当前收益率 5.3%

# 债券精确价格计算函数
def bond_price(y, F, c, T):
    t = np.arange(1, T + 1)
    pv_coupons = np.sum(c * F / (1 + y)**t)
    pv_face = F / (1 + y)**T
    return pv_coupons + pv_face

# Macaulay 久期计算函数
def mac_duration(y, F, c, T):
    P = bond_price(y, F, c, T)
    t = np.arange(1, T + 1)
    w_coupons = np.sum(t * c * F / (1 + y)**t)
    w_face = T * F / (1 + y)**T
    return (w_coupons + w_face) / P

# 当前状态计算
P0 = bond_price(y0, F, c, T)
MacD0 = mac_duration(y0, F, c, T)
ModD0 = MacD0 / (1 + y0)  # 修正久期

# 1. 计算100个基点上升后的精确价格
y_up100 = y0 + 0.01
P_up100 = bond_price(y_up100, F, c, T)

# 2. 计算用久期估计的相对价格变化
dur_approx_change_up100bp = -ModD0 * 0.01

# 3. 绘图准备
yields = np.linspace(0.02, 0.09, 700)
exact_prices = [bond_price(y, F, c, T) for y in yields]

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)

# 绘制精确价格曲线
ax.plot(yields * 100, exact_prices, 'b-', linewidth=2.5, label='精确价格')

# 绘制久期近似曲线 (初始展示全区间，后续由滑块控制展示范围)
amp_init = 3.5  # 初始变动幅度百分比 (涵盖 5.3% - 3.5% 到 5.3% + 3.5%)
yields_approx_init = np.linspace(y0 - amp_init/100, y0 + amp_init/100, 400)
approx_prices_init = P0 - ModD0 * P0 * (yields_approx_init - y0)
line_approx, = ax.plot(yields_approx_init * 100, approx_prices_init, 'r--', linewidth=2.5, label='久期近似')

# 标记当前收益率点
ax.plot(y0 * 100, P0, 'ko', markersize=8, label=f'当前状态 (y={y0*100}%)')

ax.set_xlabel('收益率 (%)', fontsize=12)
ax.set_ylabel('债券价格', fontsize=12)
ax.set_title('债券价格随收益率变化曲线及久期近似', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle=':', alpha=0.7)

# 添加滑块：调整收益率变动幅度
ax_amp = plt.axes([0.2, 0.05, 0.6, 0.03])
slider_amp = Slider(ax_amp, '收益率变动幅度 (%)', 0.1, 7.0, valinit=amp_init, valstep=0.1)

def update(val):
    amp = slider_amp.val / 100.0
    yields_approx_new = np.linspace(y0 - amp, y0 + amp, 400)
    # 截断超出2%-9%区间的部分
    yields_approx_new = yields_approx_new[(yields_approx_new >= 0.02) & (yields_approx_new <= 0.09)]
    approx_prices_new = P0 - ModD0 * P0 * (yields_approx_new - y0)
    line_approx.set_xdata(yields_approx_new * 100)
    line_approx.set_ydata(approx_prices_new)
    fig.canvas.draw_idle()

slider_amp.on_changed(update)

# 保存图表
fig_path = 'bond_price_vs_yield.png'
fig.savefig(fig_path, dpi=150, bbox_inches='tight')

# 4. 构建输出契约字典
result = {
    'price_at_up100bp': P_up100,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': fig_path
}

# 打印结果以供核对
print(f"当前收益率 (5.3%) 下的精确价格: {P0:.4f}")
print(f"当前修正久期 (Modified Duration): {ModD0:.4f}")
print(f"收益率上升100bp后的精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期估计的相对价格变化: {result['dur_approx_change_up100bp']:.4%}")
print(f"图表已保存至: {result['figure_path']}")
print("\nresult 字典内容:")
print(result)
