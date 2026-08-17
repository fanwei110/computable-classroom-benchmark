import numpy as np
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端，保证在无GUI环境下也能正常保存图片
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ==================== 债券参数 ====================
face_value = 100.0           # 面值
coupon_rate = 0.046          # 票息率 4.6%
n_years = 7                  # 期限 7 年
current_yield = 0.053        # 当前收益率 5.3%

# ==================== 现金流构造 ====================
coupon_pmt = face_value * coupon_rate
# 前 6 年为票息，第 7 年为票息+本金
cash_flows = np.array([coupon_pmt] * (n_years - 1) + [coupon_pmt + face_value])
time_periods = np.arange(1, n_years + 1)

# ==================== 核心计算函数 ====================
def bond_price(yield_rate):
    """计算给定收益率下的债券精确价格"""
    return np.sum(cash_flows / (1 + yield_rate) ** time_periods)

# 计算当前价格
P0 = bond_price(current_yield)

# 计算麦考利久期与修正久期
pv_cash_flows = cash_flows / (1 + current_yield) ** time_periods
mac_duration = np.sum(time_periods * pv_cash_flows) / P0
mod_duration = mac_duration / (1 + current_yield)

# ==================== 任务要求计算 ====================
# 1. 收益率上升 100 个基点 (1%) 后的精确价格
yield_up_100bp = current_yield + 0.01
price_up_100bp = bond_price(yield_up_100bp)

# 2. 久期法估计的相对价格变化 (ΔP/P ≈ -ModD × Δy)
delta_y_100bp = 0.01
dur_approx_relative_change = -mod_duration * delta_y_100bp

# ==================== 绘制价格-收益率曲线 ====================
# 生成 2% 到 9% 的收益率序列
yields_range = np.linspace(0.02, 0.09, 1000)
exact_prices = np.array([bond_price(y) for y in yields_range])

# 基于久期的近似价格曲线 (仅在当前收益率附近有较好近似)
# P_approx = P0 * (1 - ModD * (y - y0))
dur_approx_prices = P0 * (1 - mod_duration * (yields_range - current_yield))

# 创建画布及子图布局（为底部滑块留出空间）
fig, ax = plt.subplots(figsize=(10, 7))
plt.subplots_adjust(bottom=0.2)

# 绘制精确曲线与久期近似直线
ax.plot(yields_range * 100, exact_prices, label='Exact Price-Yield Curve', color='blue', linewidth=2)
ax.plot(yields_range * 100, dur_approx_prices, label='Duration-based Approximation', color='red', linestyle='--', linewidth=2)

# 标出当前收益率位置
current_yield_pct = current_yield * 100
ax.plot(current_yield_pct, P0, 'ko', markersize=8, 
        label=f'Current Point (Y={current_yield_pct:.1f}%, P={P0:.2f})')

ax.set_xlabel('Yield to Maturity (%)', fontsize=12)
ax.set_ylabel('Bond Price', fontsize=12)
ax.set_title('Price-Yield Curve and Duration Approximation', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle=':', alpha=0.7)

# ==================== 收益率变动幅度可调滑块 ====================
# 添加滑块，用于调整以当前收益率为中心的可视变动幅度
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
# 默认变动幅度 3.3%，使得初始视野大约为 2% ~ 8.6%
slider = Slider(ax_slider, 'Yield Range (±%)', 0.5, 10.0, valinit=3.3, valstep=0.1)

def update(val):
    """滑块回调函数，动态调整图表的X轴显示范围"""
    delta = slider.val
    ax.set_xlim(current_yield_pct - delta, current_yield_pct + delta)
    fig.canvas.draw_idle()

slider.on_changed(update)
update(3.3)  # 初始化视野范围

# 保存图表
fig_path = 'price_yield_curve.png'
plt.savefig(fig_path, dpi=150, bbox_inches='tight')

# ==================== 输出契约 ====================
result = {
    'price_at_up100bp': price_up_100bp,
    'dur_approx_change_up100bp': dur_approx_relative_change,
    'figure_path': fig_path
}

# 打印结果便于确认
print("Result Dictionary:")
for k, v in result.items():
    if isinstance(v, float):
        print(f"  '{k}': {v:.6f}")
    else:
        print(f"  '{k}': {v}")
