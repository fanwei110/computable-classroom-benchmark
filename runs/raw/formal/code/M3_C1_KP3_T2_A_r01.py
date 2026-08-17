import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ------------ 债券参数 ------------
F = 100          # 面值
c_rate = 0.046   # 票息率
C = F * c_rate    # 票息
T = 7            # 期限
y0 = 0.053       # 当前收益率

# ------------ 核心计算函数 ------------
def bond_price(y):
    """计算债券精确价格"""
    t = np.arange(1, T + 1)
    pv_coupons = np.sum(C / (1 + y)**t)
    pv_face = F / (1 + y)**T
    return pv_coupons + pv_face

def calc_duration(y):
    """计算修正久期"""
    t = np.arange(1, T + 1)
    cf = np.full(T, C)
    cf[-1] += F
    pv_cf = cf / (1 + y)**t
    P = np.sum(pv_cf)
    mac_dur = np.sum(t * pv_cf) / P
    mod_dur = mac_dur / (1 + y)
    return mod_dur

# ------------ 基础数据计算 ------------
P0 = bond_price(y0)
mod_dur = calc_duration(y0)

# 1. 收益率上升100个基点后的精确价格
y_up_100bp = y0 + 0.01
price_at_up100bp = bond_price(y_up_100bp)

# 2. 用久期估的相对价格变化
dur_approx_change_up100bp = -mod_dur * 0.01

# ------------ 绘图数据 ------------
y_range = np.linspace(0.02, 0.09, 500)
exact_prices = [bond_price(y) for y in y_range]
# 久期近似：P_approx = P0 * (1 - ModDur * (y - y0))
approx_prices = P0 * (1 - mod_dur * (y_range - y0))

# ------------ 绘图与交互 ------------
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)

# 绘制精确曲线和久期近似直线
l_exact, = ax.plot(y_range * 100, exact_prices, 'b-', linewidth=2, label='精确价格 (Exact Price)')
l_approx, = ax.plot(y_range * 100, approx_prices, 'r--', linewidth=2, label='久期近似 (Duration Approx)')

# 标记初始基点
ax.plot(y0 * 100, P0, 'ko', label='初始基点 (y=5.3%)')

# 初始设置：收益率变动幅度为 +100bp
init_delta_y = 0.01
y_new = y0 + init_delta_y
p_exact_new = bond_price(y_new)
p_approx_new = P0 * (1 - mod_dur * init_delta_y)

# 画动态指示线和点
vline = ax.axvline(x=y_new * 100, color='gray', linestyle=':', linewidth=1)
hline_exact = ax.axhline(y=p_exact_new, color='b', linestyle=':', linewidth=1, alpha=0.5)
hline_approx = ax.axhline(y=p_approx_new, color='r', linestyle=':', linewidth=1, alpha=0.5)
dot_exact, = ax.plot(y_new * 100, p_exact_new, 'bo', markersize=8)
dot_approx, = ax.plot(y_new * 100, p_approx_new, 'r^', markersize=8)

# 动态文本框
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
info_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10,
                    verticalalignment='top', bbox=props)

ax.set_xlabel('收益率 Yield (%)')
ax.set_ylabel('债券价格 Price')
ax.set_title('债券价格随收益率变化曲线 (精确 vs 久期近似)')
ax.legend(loc='upper right')
ax.grid(True, linestyle='--', alpha=0.6)

# 添加滑块：收益率变动幅度（基点）
ax_slider = plt.axes([0.15, 0.05, 0.7, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, '收益率变动 (bp)', -300, 300, valinit=100, valstep=10)

def update(val):
    dy = slider.val / 10000.0
    y_new = y0 + dy
    p_exact_new = bond_price(y_new)
    p_approx_new = P0 * (1 - mod_dur * dy)
    
    # 更新指示线
    vline.set_xdata([y_new * 100, y_new * 100])
    hline_exact.set_ydata([p_exact_new, p_exact_new])
    hline_approx.set_ydata([p_approx_new, p_approx_new])
    
    # 更新点
    dot_exact.set_xdata([y_new * 100])
    dot_exact.set_ydata([p_exact_new])
    dot_approx.set_xdata([y_new * 100])
    dot_approx.set_ydata([p_approx_new])
    
    # 更新文本
    approx_pct_change = -mod_dur * dy
    text_str = (f"当前Δy: {slider.val}bp\n"
                f"精确价格: {p_exact_new:.4f}\n"
                f"久期近似相对变化: {approx_pct_change*100:.2f}%")
    info_text.set_text(text_str)
    
    fig.canvas.draw_idle()

slider.on_changed(update)
# 初始化触发一次
update(100)

# 保存图像
fig_path = 'bond_price_yield_curve.png'
fig.savefig(fig_path, dpi=150)
plt.close(fig)

# ------------ 输出契约组装 ------------
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': fig_path
}

# 打印结果供查验
print(result)
