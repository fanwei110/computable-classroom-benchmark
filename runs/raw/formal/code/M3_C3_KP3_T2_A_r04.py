import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def bond_price(y, F, c, T):
    """计算债券精确价格（年复利）"""
    if y == 0:
        return F + F * c * T
    C = F * c
    pv_coupons = C * (1 - (1+y)**-T) / y
    pv_face = F * (1+y)**-T
    return pv_coupons + pv_face

# 债券基本参数
F = 100
c = 0.046
T = 7
y0 = 0.053

# 计算初始价格及久期
P0 = bond_price(y0, F, c, T)

# 麦考利久期
MD = (sum([t * F*c / (1+y0)**t for t in range(1, T+1)]) + T * F / (1+y0)**T) / P0
# 修正久期
ModD = MD / (1 + y0)

# 生成收益率从 2% 到 9% 的曲线数据
y_min, y_max = 0.02, 0.09
yields = np.linspace(y_min, y_max, 500)
exact_prices = np.array([bond_price(y, F, c, T) for y in yields])
# 久期近似价格 (在 y0 处的切线)
approx_prices = P0 - ModD * P0 * (yields - y0)

# 绘图设置
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)

# 绘制精确与近似曲线
ax.plot(yields * 100, exact_prices, label='精确价格', color='blue', linewidth=2)
ax.plot(yields * 100, approx_prices, label='久期近似', color='red', linestyle='--', linewidth=2)
ax.axvline(x=y0*100, color='gray', linestyle=':', label='当前收益率 (5.3%)')

# 增加可调的收益率变动幅度区间 (默认展示100bp变动幅度)
span = ax.axvspan(y0*100 - 1.0, y0*100 + 1.0, color='green', alpha=0.2, label='变动幅度区间')

ax.set_xlabel('收益率 (%)')
ax.set_ylabel('债券价格')
ax.set_title('债券价格随收益率变化曲线及久期近似')
ax.legend(loc='upper right')
ax.grid(True)

# 添加滑块：使收益率变动幅度可调
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
slider = Slider(ax_slider, '变动幅度(%)', 0.1, 3.3, valinit=1.0, valstep=0.1)

def update(val):
    dy = slider.val
    # 更新绿色阴影区间的边界
    xy = np.array([[y0*100 - dy, 0], [y0*100 - dy, 1], 
                   [y0*100 + dy, 1], [y0*100 + dy, 0], [y0*100 - dy, 0]])
    span.set_xy(xy)
    fig.canvas.draw_idle()

slider.on_changed(update)

# 保存图像
figure_path = "bond_price_yield_curve.png"
plt.savefig(figure_path)

# ================= 计算要求报告的数值 =================
y_up100bp = y0 + 0.01
price_at_up100bp = bond_price(y_up100bp, F, c, T)
dur_approx_change_up100bp = -ModD * 0.01

result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}
