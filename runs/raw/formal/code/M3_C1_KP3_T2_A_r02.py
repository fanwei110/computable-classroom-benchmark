import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# --- 债券参数 ---
F = 100          # 面值
C_rate = 0.046   # 票息率
T = 7            # 期限
y0 = 0.053       # 当前收益率
coupon = F * C_rate

# --- 计算函数 ---
def bond_price(y):
    """精确债券价格计算"""
    pv_coupons = coupon * (1 - (1 + y)**(-T)) / y
    pv_face = F * (1 + y)**(-T)
    return pv_coupons + pv_face

def mac_duration(y):
    """计算麦考利久期"""
    P0 = bond_price(y)
    times = np.arange(1, T + 1)
    pv_cf = (times * coupon) / (1 + y)**times
    pv_face = T * F / (1 + y)**T
    return (np.sum(pv_cf) + pv_face) / P0

# --- 核心指标计算 ---
# 1. 收益率上升100个基点后的精确价格
y_up100 = y0 + 0.01
price_at_up100bp = bond_price(y_up100)

# 2. 久期估计的相对价格变化
mac_d = mac_duration(y0)
mod_d = mac_d / (1 + y0)  # 修正久期
dur_approx_change_up100bp = -mod_d * 0.01

# --- 绘图准备 ---
yields = np.linspace(0.02, 0.09, 300)
exact_prices = bond_price(yields)
P0 = bond_price(y0)

# 久期近似线（切线）
approx_prices_tangent = P0 - P0 * mod_d * (yields - y0)

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.25) # 为底部滑块留出空间

# 绘制曲线
line_exact, = ax.plot(yields * 100, exact_prices, 'b-', linewidth=2, label='精确价格')
line_approx, = ax.plot(yields * 100, approx_prices_tangent, 'r--', linewidth=2, label='久期近似')

# 初始化标记点（收益率变动幅度为0时重合）
point_exact, = ax.plot(y0 * 100, P0, 'bo', markersize=8, zorder=5)
point_approx, = ax.plot(y0 * 100, P0, 'ro', markersize=8, zorder=5)
vline = ax.axvline(x=y0 * 100, color='gray', linestyle=':', alpha=0.6)

ax.set_xlabel('收益率 (%)', fontdict={'family': 'SimHei', 'size': 12})
ax.set_ylabel('债券价格', fontdict={'family': 'SimHei', 'size': 12})
ax.set_title('债券价格随收益率变化曲线 (精确 vs 久期近似)', fontdict={'family': 'SimHei', 'size': 14})
ax.legend(prop={'family': 'SimHei', 'size': 12})
ax.grid(True, linestyle='--', alpha=0.5)

# --- 添加可调滑块（收益率变动幅度） ---
ax_slider = plt.axes([0.25, 0.1, 0.5, 0.03])
# 变动幅度范围设为 -300bp 到 +300bp
slider = Slider(
    ax=ax_slider, 
    label='收益率变动幅度', 
    valmin=-300, 
    valmax=300, 
    valinit=0, 
    valstep=10,
    valfmt='%1.0f bp'
)

def update(val):
    delta_bp = slider.val
    delta_y = delta_bp / 10000
    y_new = y0 + delta_y
    
    # 更新标记点
    exact_p = bond_price(y_new)
    approx_p = P0 - P0 * mod_d * delta_y
    
    point_exact.set_ydata([exact_p])
    point_exact.set_xdata([y_new * 100])
    point_approx.set_ydata([approx_p])
    point_approx.set_xdata([y_new * 100])
    vline.set_xdata([y_new * 100])
    
    fig.canvas.draw_idle()

slider.on_changed(update)

# --- 保存与输出 ---
figure_path = 'bond_price_vs_yield.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')

# 组装输出契约字典
result = {
    'price_at_up100bp': round(price_at_up100bp, 6),
    'dur_approx_change_up100bp': round(dur_approx_change_up100bp, 6),
    'figure_path': figure_path
}

# 打印结果供查看
print(result)

# 取消下行注释即可使用交互式滑块查看不同变动幅度下的价格差异
# plt.show()
