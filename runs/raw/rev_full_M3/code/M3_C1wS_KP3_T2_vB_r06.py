import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 债券参数设置
# ==========================================
FACE_VALUE = 100.0         # 面值
COUPON_RATE = 0.046        # 票息率 4.6%
MATURITY = 7               # 期限 7年
YTM_BASE = 0.053           # 基准收益率 5.3%
DELTA_Y = 0.01             # 变动幅度 (可调，此处为+100bp)

# ==========================================
# 现金流构建
# ==========================================
t_arr = np.arange(1, MATURITY + 1)
cf_arr = np.full(MATURITY, FACE_VALUE * COUPON_RATE)
cf_arr[-1] += FACE_VALUE   # 最后一期加入面值

# ==========================================
# 核心计算函数
# ==========================================
def bond_price(ytm):
    """精确计算债券价格"""
    return np.sum(cf_arr / (1 + ytm)**t_arr)

def modified_duration(ytm):
    """计算修正久期"""
    P = bond_price(ytm)
    mac_dur = np.sum(t_arr * cf_arr / (1 + ytm)**t_arr) / P
    return mac_dur / (1 + ytm)

def convexity(ytm):
    """计算凸性"""
    P = bond_price(ytm)
    return np.sum(t_arr * (t_arr + 1) * cf_arr / (1 + ytm)**t_arr) / (P * (1 + ytm)**2)

# ==========================================
# 基准点与目标点计算
# ==========================================
P0 = bond_price(YTM_BASE)
MD0 = modified_duration(YTM_BASE)
CONV0 = convexity(YTM_BASE)

# +100bp 后的精确价格
y_up = YTM_BASE + DELTA_Y
price_at_up100bp = bond_price(y_up)

# 久期法估计的相对变化
dur_approx_change_up100bp = -MD0 * DELTA_Y

# ==========================================
# 价格-收益率曲线网格计算
# ==========================================
y_grid = np.linspace(0.02, 0.09, 700)
price_exact = np.array([bond_price(y) for y in y_grid])

# 基于基准点的久期近似与久期+凸性近似
price_dur_approx = P0 * (1 - MD0 * (y_grid - YTM_BASE))
price_conv_approx = P0 * (1 - MD0 * (y_grid - YTM_BASE) + 0.5 * CONV0 * (y_grid - YTM_BASE)**2)

# ==========================================
# 绘图设置
# ==========================================
# 使用英文标签以确保在任何操作系统环境下绘图均不出现中文乱码
plt.figure(figsize=(10, 6))
plt.plot(y_grid * 100, price_exact, label='Exact Price', color='blue', linewidth=2)
plt.plot(y_grid * 100, price_dur_approx, label='Duration Approximation', color='red', linestyle='--')
plt.plot(y_grid * 100, price_conv_approx, label='Duration + Convexity Approximation', color='green', linestyle=':')

# 标出基准点和+100bp的精确点
plt.scatter([YTM_BASE * 100], [P0], color='black', zorder=5, label=f'Base Point (YTM={YTM_BASE*100:.1f}%)')
plt.scatter([y_up * 100], [price_at_up100bp], color='purple', zorder=5, marker='x', s=100, label=f'+100bp Exact Price')

plt.title('Price-Yield Curve and Approximations')
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Bond Price')
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.6)

# 保存图形
fig_path = 'bond_price_yield_curve.png'
plt.savefig(fig_path, dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 结果封装
# ==========================================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': fig_path
}

# 打印结果以便课堂投屏展示
print(f"基准 YTM ({YTM_BASE*100:.1f}%) 下的精确价格: {P0:.4f}")
print(f"基准 YTM 下的修正久期: {MD0:.4f}")
print(f"基准 YTM 下的凸性: {CONV0:.4f}")
print("-" * 50)
print(f"收益率上升 {DELTA_Y*100:.0f}bp 后:")
print(f"  精确价格: {result['price_at_up100bp']:.4f}")
print(f"  久期法估计的相对变化: {result['dur_approx_change_up100bp']:.4%}")
print("-" * 50)
print(f"图形已保存至: {result['figure_path']}")
