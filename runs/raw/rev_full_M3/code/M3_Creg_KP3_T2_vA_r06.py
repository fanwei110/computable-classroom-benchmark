import numpy as np
import matplotlib.pyplot as plt

# ================= 债券参数 =================
FACE_VALUE = 100
COUPON_RATE = 0.046
YEARS_TO_MATURITY = 7
CURRENT_YIELD = 0.053

# ================= 可调参数 =================
# 收益率变动幅度（此处设为100个基点，可自由调整以观察不同冲击下的结果）
YIELD_SHIFT_BPS = 100
YIELD_SHIFT = YIELD_SHIFT_BPS / 10000

# 久期近似曲线在当前收益率附近显示的变动范围（上下对称，单位：小数形式）
APPROX_DISPLAY_SPAN = 0.03  

# ================= 核心计算函数 =================
def bond_prices(yield_rates, face_value, coupon_rate, years):
    """
    向量化计算债券精确价格
    yield_rates: 收益率数组或标量
    """
    C = face_value * coupon_rate
    # 构造时间向量用于向量化折现
    t = np.arange(1, years + 1).reshape(-1, 1)
    yields = np.array(yield_rates).reshape(1, -1)
    
    pv_coupons = np.sum(C / (1 + yields)**t, axis=0)
    pv_face = face_value / (1 + yields)**years
    return pv_coupons + pv_face

def calc_duration_and_price(yield_rate, face_value, coupon_rate, years):
    """计算给定收益率下的麦考利久期与精确价格"""
    C = face_value * coupon_rate
    P0 = bond_prices([yield_rate], face_value, coupon_rate, years)[0]
    
    t = np.arange(1, years + 1)
    # 构造现金流，最后一期包含本金
    cf = np.full(years, C)
    cf[-1] += face_value
    
    pv_cf = cf / (1 + yield_rate)**t
    D_mac = np.sum(t * pv_cf) / P0
    return D_mac, P0

# ================= 计算当前指标 =================
D_mac, P0 = calc_duration_and_price(CURRENT_YIELD, FACE_VALUE, COUPON_RATE, YEARS_TO_MATURITY)
D_mod = D_mac / (1 + CURRENT_YIELD)  # 修正久期

# 1. 收益率上升 100 个基点后的精确价格
yield_up = CURRENT_YIELD + YIELD_SHIFT
price_at_up100bp = bond_prices([yield_up], FACE_VALUE, COUPON_RATE, YEARS_TO_MATURITY)[0]

# 2. 久期法估计的相对价格变化
dur_approx_change_up100bp = -D_mod * YIELD_SHIFT

# ================= 绘图 =================
# 生成从 2% 到 9% 的精确价格-收益率曲线数据
yields_exact = np.linspace(0.02, 0.09, 700)
prices_exact = bond_prices(yields_exact, FACE_VALUE, COUPON_RATE, YEARS_TO_MATURITY)

# 生成当前收益率附近的久期近似数据（基于可调变动幅度）
yields_approx = np.linspace(CURRENT_YIELD - APPROX_DISPLAY_SPAN, 
                             CURRENT_YIELD + APPROX_DISPLAY_SPAN, 200)
prices_approx = P0 * (1 - D_mod * (yields_approx - CURRENT_YIELD))

plt.figure(figsize=(10, 6))
plt.plot(yields_exact * 100, prices_exact, label='Exact Price-Yield Curve', color='blue', linewidth=2)
plt.plot(yields_approx * 100, prices_approx, label='Duration-Based Approximation', color='red', linestyle='--', linewidth=2)

# 标记当前收益率点
plt.scatter([CURRENT_YIELD * 100], [P0], color='black', zorder=5)
plt.annotate(f'Current Yield\n({CURRENT_YIELD*100:.1f}%, {P0:.2f})', 
             xy=(CURRENT_YIELD * 100, P0), 
             xytext=(CURRENT_YIELD * 100 + 1.5, P0 + 2),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.title('Bond Price-Yield Curve and Duration Approximation')
plt.xlabel('Yield (%)')
plt.ylabel('Bond Price')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)

figure_path = 'price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ================= 结果封装 =================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 打印验证输出
print(f"当前价格: {P0:.4f}")
print(f"修正久期: {D_mod:.4f}")
print(f"收益率上升100基点后精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.4%}")
print(f"结果字典: {result}")
