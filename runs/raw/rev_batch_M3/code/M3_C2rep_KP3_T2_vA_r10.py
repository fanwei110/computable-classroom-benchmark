import numpy as np
import matplotlib.pyplot as plt

# ================= 债券参数 =================
F = 100            # 面值
coupon_rate = 0.046# 票息率
n = 7              # 期限（年）
y0 = 0.053         # 当前收益率
dy_bp = 100        # 基点变动（可调参数，如100表示100个基点）
dy = dy_bp / 10000 # 收益率变动幅度

# ================= 可调参数：久期近似线的收益率范围 =================
# 久期近似线以当前收益率 y0 为中心，向两侧延伸的范围
yield_range_offset = 0.05  

# ================= 现金流 =================
t = np.arange(1, n + 1)
cf = np.full(n, coupon_rate * F)
cf[-1] += F  # 最后一期加上面值

# ================= 1. 精确定价函数 =================
def calc_price(y_arr):
    """计算给定收益率数组下的债券精确价格"""
    y_arr = np.asarray(y_arr).reshape(-1, 1)
    pv = cf / (1 + y_arr)**t
    return pv.sum(axis=1)

# 在 2% 到 9% 的收益率网格上为精确曲线定价
y_grid = np.linspace(0.02, 0.09, 300)
p_grid = calc_price(y_grid)

# ================= 2. 当前收益率下的价格及修正久期 =================
P0 = calc_price([y0])[0]
pv_cf = cf / (1 + y0)**t
mac_dur = np.sum(t * pv_cf) / P0
mod_dur = mac_dur / (1 + y0)  # 修正久期

# 久期法近似价格：P ≈ P0 * [1 - ModDur * (y - y0)]
y_approx = np.linspace(y0 - yield_range_offset, y0 + yield_range_offset, 300)
p_approx = P0 * (1 - mod_dur * (y_approx - y0))

# ================= 3. 收益率上升100个基点的精确价格与久期估计 =================
y_up = y0 + dy
price_at_up100bp = calc_price([y_up])[0]
dur_approx_change_up100bp = -mod_dur * dy  # 久期法估计的相对价格变化

# ================= 4. 绘图与保存 =================
plt.figure(figsize=(10, 6))
plt.plot(y_grid * 100, p_grid, label='Exact Price-Yield Curve', linewidth=2)
plt.plot(y_approx * 100, p_approx, label='Duration Approximation', linestyle='--', linewidth=2)
plt.axvline(x=y0 * 100, color='gray', linestyle=':', label=f'Current Yield ({y0*100:.1f}%)')
plt.scatter([y0 * 100, y_up * 100], [P0, price_at_up100bp], color='red', zorder=5)

plt.xlabel('Yield (%)')
plt.ylabel('Price')
plt.title('Bond Price-Yield Curve and Duration Approximation')
plt.legend()
plt.grid(True)

fig_path = 'bond_price_yield_curve.png'
plt.savefig(fig_path)
plt.close()

# ================= 5. 输出契约 =================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': fig_path
}
