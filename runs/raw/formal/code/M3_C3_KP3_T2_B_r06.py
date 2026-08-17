import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- 债券参数 ---
F = 100            # 面值
c = 0.046          # 票息率 (小数表示)
T = 7              # 期限 (年)
y0 = 0.053         # 当前到期收益率 YTM (小数表示)
C = F * c          # 每年票息

# --- 收益率变动幅度 (可调) ---
yield_shift = 0.01 # 默认设定为 +100bp

# --- 定价与久期计算函数 ---
def bond_price(y, F=F, C=C, T=T):
    """精确价格计算 (按年复利)"""
    y = np.asarray(y)
    prices = np.zeros_like(y, dtype=float)
    for t in range(1, T + 1):
        prices += C / (1 + y)**t
    prices += F / (1 + y)**T
    return prices

def modified_duration(y, F=F, C=C, T=T):
    """修正久期计算"""
    y_val = np.asarray(y)
    P = bond_price(y_val, F, C, T)
    D = np.zeros_like(y_val, dtype=float)
    for t in range(1, T + 1):
        D += t * C / (1 + y_val)**t
    D += T * F / (1 + y_val)**T
    mac_duration = D / P
    return mac_duration / (1 + y_val)

# --- 计算当前指标 ---
P0 = bond_price(np.array([y0]))[0]
MD0 = modified_duration(np.array([y0]))[0]

# --- 计算要求输出 ---
# 1. 收益率+100bp后的精确价格
y_up = y0 + yield_shift
price_at_up100bp = bond_price(np.array([y_up]))[0]

# 2. 久期法估的相对变化
dur_approx_change_up100bp = -MD0 * yield_shift

# --- 画图：价格-收益率曲线 ---
y_vals = np.linspace(0.02, 0.09, 500)
P_exact_vals = bond_price(y_vals)
P_approx_vals = P0 * (1 - MD0 * (y_vals - y0))

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25)

# 绘制精确价格和久期近似曲线，图例分开
line_exact, = ax.plot(y_vals, P_exact_vals, label='Exact Price', color='blue')
line_approx, = ax.plot(y_vals, P_approx_vals, label='Duration Approximation', color='red', linestyle='--')

# 标记初始点和+100bp点
ax.plot(y0, P0, 'ko', label='Initial Point (YTM=5.3%)')
point_exact_up, = ax.plot(y_up, price_at_up100bp, 'bo', label='Exact Price at +100bp')
point_approx_up, = ax.plot(y_up, P0 * (1 + dur_approx_change_up100bp), 'rx', label='Approx Price at +100bp')

ax.set_xlabel('Yield (YTM)')
ax.set_ylabel('Price')
ax.set_title('Price-Yield Curve & Duration Approximation')
ax.legend()
ax.grid(True)

# 增加变动幅度可调的滑块
ax_shift = plt.axes([0.25, 0.1, 0.5, 0.03])
slider_shift = Slider(ax_shift, 'Yield Shift', 0.0, 0.05, valinit=yield_shift, valstep=0.001)

def update(val):
    shift = slider_shift.val
    y_new = y0 + shift
    p_exact_new = bond_price(np.array([y_new]))[0]
    p_approx_new = P0 * (1 - MD0 * shift)
    
    point_exact_up.set_xdata([y_new])
    point_exact_up.set_ydata([p_exact_new])
    point_approx_up.set_xdata([y_new])
    point_approx_up.set_ydata([p_approx_new])
    fig.canvas.draw_idle()

slider_shift.on_changed(update)

# 保存图片
figure_path = 'price_yield_curve.png'
plt.savefig(figure_path)

# --- 存入结果 ---
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

print(result)
