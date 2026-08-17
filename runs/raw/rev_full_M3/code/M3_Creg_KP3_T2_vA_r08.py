import numpy as np
import matplotlib.pyplot as plt
import os

# ==========================================
# 可调参数：收益率变动幅度（用于久期近似线绘制范围）
# ==========================================
YIELD_CHANGE_AMPLITUDE = 0.015  # +/- 1.5% (150个基点)

# ==========================================
# 债券固定参数
# ==========================================
FACE_VALUE = 100.0
COUPON_RATE = 0.046
MATURITY = 7
CURRENT_YIELD = 0.053

# ==========================================
# 核心计算函数
# ==========================================
def bond_price(face_value: float, coupon_rate: float, maturity: int, yield_rate: float) -> float:
    """
    计算债券的精确价格（假设年付息）
    """
    coupon = face_value * coupon_rate
    if yield_rate == 0.0:
        return coupon * maturity + face_value
    
    pv_coupons = coupon * (1 - (1 + yield_rate)**(-maturity)) / yield_rate
    pv_face = face_value * (1 + yield_rate)**(-maturity)
    return pv_coupons + pv_face

def calc_macaulay_duration(face_value: float, coupon_rate: float, maturity: int, yield_rate: float) -> float:
    """
    计算麦考利久期
    """
    coupon = face_value * coupon_rate
    price = bond_price(face_value, coupon_rate, maturity, yield_rate)
    
    t_arr = np.arange(1, maturity + 1)
    cf_arr = np.full(maturity, coupon)
    cf_arr[-1] += face_value  # 最后一期包含本金
    
    pv_cf_arr = cf_arr / (1 + yield_rate)**t_arr
    mac_dur = np.sum(t_arr * pv_cf_arr) / price
    return mac_dur

# ==========================================
# 计算当前状态与久期
# ==========================================
current_price = bond_price(FACE_VALUE, COUPON_RATE, MATURITY, CURRENT_YIELD)
macaulay_duration = calc_macaulay_duration(FACE_VALUE, COUPON_RATE, MATURITY, CURRENT_YIELD)
modified_duration = macaulay_duration / (1 + CURRENT_YIELD)

# ==========================================
# 1. 精确价格-收益率曲线
# ==========================================
yields_exact = np.linspace(0.02, 0.09, 1000)
prices_exact = np.array([bond_price(FACE_VALUE, COUPON_RATE, MATURITY, y) for y in yields_exact])

# ==========================================
# 2. 久期法近似曲线
# ==========================================
yields_dur = np.linspace(CURRENT_YIELD - YIELD_CHANGE_AMPLITUDE, 
                         CURRENT_YIELD + YIELD_CHANGE_AMPLITUDE, 
                         100)
# 久期近似公式: P_approx = P0 * (1 - ModDur * (y - y0))
prices_dur_approx = current_price * (1 - modified_duration * (yields_dur - CURRENT_YIELD))

# ==========================================
# 3. 绘图
# ==========================================
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(yields_exact * 100, prices_exact, 
        label='Exact Price-Yield Curve', color='blue', linewidth=2)
ax.plot(yields_dur * 100, prices_dur_approx, 
        label='Duration-Based Approximation', color='red', linestyle='--', linewidth=2)
ax.scatter([CURRENT_YIELD * 100], [current_price], 
           color='black', zorder=5, label=f'Current Yield ({CURRENT_YIELD*100:.1f}%)')

ax.set_xlabel('Yield (%)', fontsize=12)
ax.set_ylabel('Price', fontsize=12)
ax.set_title('Bond Price-Yield Curve and Duration Approximation', fontsize=14)
ax.legend(fontsize=11)
ax.grid(True, linestyle=':', alpha=0.7)

# 保存图片
figure_path = 'price_yield_curve.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ==========================================
# 4. 特定场景报告
# ==========================================
# 收益率上升 100 个基点 (1%)
yield_up_100bp = CURRENT_YIELD + 0.01
price_at_up100bp = bond_price(FACE_VALUE, COUPON_RATE, MATURITY, yield_up_100bp)

# 久期法估计的相对价格变化
delta_y = 0.01
dur_approx_relative_change = -modified_duration * delta_y

# ==========================================
# 5. 结果封装
# ==========================================
result = {
    'price_at_up100bp': round(price_at_up100bp, 6),
    'dur_approx_change_up100bp': round(dur_approx_relative_change, 6),
    'figure_path': figure_path
}

# 打印结果以便验证
print("Result Dictionary:")
for k, v in result.items():
    print(f"{k}: {v}")
