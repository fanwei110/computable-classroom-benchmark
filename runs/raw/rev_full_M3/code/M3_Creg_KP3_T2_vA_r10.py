import numpy as np
import matplotlib.pyplot as plt

# ==================== 债券参数 ====================
FACE_VALUE = 100.0        # 面值
COUPON_RATE = 0.046       # 票息率 4.6%
MATURITY = 7              # 期限 7 年
CURRENT_YIELD = 0.053     # 当前收益率 5.3%

# ==================== 可调参数 ====================
# 收益率变动幅度（绘图步长与范围）
YIELD_PLOT_MIN = 0.02     # 绘图最低收益率 2%
YIELD_PLOT_MAX = 0.09     # 绘图最高收益率 9%
YIELD_PLOT_STEP = 0.0005  # 收益率变动步长（可调：控制曲线平滑度与计算密度）

# ==================== 核心计算函数 ====================
def calculate_bond_price(face_value, coupon_rate, maturity, yields):
    """
    计算债券的精确价格。
    支持 yields 为标量或 numpy 数组（用于向量化绘图）。
    假设每年付息一次，按复利贴现。
    """
    is_scalar = np.isscalar(yields)
    yields = np.atleast_1d(np.asarray(yields, dtype=float))
    
    periods = np.arange(1, maturity + 1)
    coupon_pmt = face_value * coupon_rate
    
    # 利用广播机制计算各期票息的现值
    pv_coupons = np.sum(coupon_pmt / (1 + yields[:, None])**periods, axis=1)
    # 面值的现值
    pv_face = face_value / (1 + yields)**maturity
    prices = pv_coupons + pv_face
    
    return float(prices[0]) if is_scalar else prices

def calculate_duration(face_value, coupon_rate, maturity, yield_rate):
    """
    计算给定收益率下的麦考利久期与修正久期。
    """
    periods = np.arange(1, maturity + 1)
    coupon_pmt = face_value * coupon_rate
    price = calculate_bond_price(face_value, coupon_rate, maturity, yield_rate)
    
    # 各期现金流现值
    pv_cash_flows = coupon_pmt / (1 + yield_rate)**periods
    pv_cash_flows[-1] += face_value / (1 + yield_rate)**maturity
    
    # 麦考利久期
    mac_duration = np.sum(periods * pv_cash_flows) / price
    # 修正久期
    mod_duration = mac_duration / (1 + yield_rate)
    
    return mac_duration, mod_duration

# ==================== 数据计算 ====================
# 1. 当前收益率下的精确价格与久期
current_price = calculate_bond_price(FACE_VALUE, COUPON_RATE, MATURITY, CURRENT_YIELD)
mac_dur, mod_dur = calculate_duration(FACE_VALUE, COUPON_RATE, MATURITY, CURRENT_YIELD)

# 2. 生成收益率网格（通过 YIELD_PLOT_STEP 控制变动幅度/步长）
yields_grid = np.arange(YIELD_PLOT_MIN, YIELD_PLOT_MAX + YIELD_PLOT_STEP, YIELD_PLOT_STEP)

# 3. 计算精确价格曲线
exact_prices = calculate_bond_price(FACE_VALUE, COUPON_RATE, MATURITY, yields_grid)

# 4. 计算基于久期的近似价格曲线
# 近似公式: P_approx = P0 * (1 - ModDur * (y - y0))
delta_y = yields_grid - CURRENT_YIELD
approx_prices = current_price * (1 - mod_dur * delta_y)

# 5. 收益率上升 100 个基点 (1%) 后的精确价格
yield_up_100bp = CURRENT_YIELD + 0.01
price_at_up100bp = calculate_bond_price(FACE_VALUE, COUPON_RATE, MATURITY, yield_up_100bp)

# 6. 久期法估计的相对价格变化 (上升100基点)
# 公式: ΔP/P ≈ -ModDur * Δy
dur_approx_change_up100bp = -mod_dur * 0.01

# ==================== 绘图 ====================
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 兼容中文
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

# 绘制精确价格-收益率曲线
ax.plot(yields_grid * 100, exact_prices, 
        label='Exact Price-Yield Curve', 
        color='blue', linewidth=2)

# 叠加基于久期的近似直线
ax.plot(yields_grid * 100, approx_prices, 
        label='Duration-Based Approximation', 
        color='red', linestyle='--', linewidth=2)

# 标出当前收益率所在的点
ax.plot(CURRENT_YIELD * 100, current_price, 'go', markersize=8, 
        label=f'Current Yield Point ({CURRENT_YIELD*100:.1f}%)')

ax.set_title('Bond Price-Yield Relationship and Duration Approximation', fontsize=14)
ax.set_xlabel('Yield (%)', fontsize=12)
ax.set_ylabel('Price', fontsize=12)
ax.legend(fontsize=10)
ax.grid(True, linestyle=':', alpha=0.7)

# 保存图表
figure_path = 'price_yield_curve.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ==================== 输出契约组装 ====================
result = {
    'price_at_up100bp': round(float(price_at_up100bp), 6),
    'dur_approx_change_up100bp': round(float(dur_approx_change_up100bp), 6),
    'figure_path': figure_path
}

# 打印结果以便验证
if __name__ == '__main__':
    print(f"当前收益率 ({CURRENT_YIELD*100:.1f}%) 下债券精确价格: {current_price:.4f}")
    print(f"修正久期: {mod_dur:.4f}")
    print(f"收益率上升100bp后精确价格: {result['price_at_up100bp']}")
    print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']}")
    print(f"图表已保存至: {result['figure_path']}")
