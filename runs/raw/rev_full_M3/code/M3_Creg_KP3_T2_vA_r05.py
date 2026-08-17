import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 可调参数区
# ==========================================
# 当前收益率附近基于久期近似的收益率变动幅度（左右各多少），可按需调整
APPROX_SHIFT_RANGE = 0.04  # 例如 4%，即当前收益率上下各 4% 的范围画近似线

# ==========================================
# 债券基本参数
# ==========================================
FACE_VALUE = 100           # 面值
COUPON_RATE = 0.046        # 票息率 4.6%
MATURITY = 7               # 期限 7 年
CURRENT_YIELD = 0.053      # 当前收益率 5.3%
YIELD_SHIFT_100BP = 0.01   # 收益率上升 100 个基点 (1%)

# ==========================================
# 核心计算函数（假设年度付息）
# ==========================================
def bond_price(face_value, coupon_rate, maturity, ytm):
    """计算债券的精确价格"""
    periods = np.arange(1, maturity + 1)
    coupon = face_value * coupon_rate
    pv_coupons = np.sum(coupon / (1 + ytm) ** periods)
    pv_face = face_value / (1 + ytm) ** maturity
    return pv_coupons + pv_face

def bond_modified_duration(face_value, coupon_rate, maturity, ytm):
    """计算修正久期 (Modified Duration)"""
    periods = np.arange(1, maturity + 1)
    coupon = face_value * coupon_rate
    cash_flows = np.full(maturity, coupon)
    cash_flows[-1] += face_value
    
    pv_cash_flows = cash_flows / (1 + ytm) ** periods
    price = np.sum(pv_cash_flows)
    
    # 麦考利久期
    mac_duration = np.sum(periods * pv_cash_flows) / price
    # 修正久期
    mod_duration = mac_duration / (1 + ytm)
    return mod_duration

# ==========================================
# 任务 1: 计算当前状态及久期
# ==========================================
P0 = bond_price(FACE_VALUE, COUPON_RATE, MATURITY, CURRENT_YIELD)
MD0 = bond_modified_duration(FACE_VALUE, COUPON_RATE, MATURITY, CURRENT_YIELD)

# ==========================================
# 任务 2: 报告收益率上升 100 基点后的精确价格及久期法相对变化
# ==========================================
price_at_up100bp = bond_price(FACE_VALUE, COUPON_RATE, MATURITY, CURRENT_YIELD + YIELD_SHIFT_100BP)

# 久期法估计的相对价格变化: ΔP/P ≈ -MD * Δy
dur_approx_change_up100bp = -MD0 * YIELD_SHIFT_100BP

# ==========================================
# 任务 3: 绘制精确价格-收益率曲线与久期近似线
# ==========================================
# 收益率从 2% 到 9%
y_grid = np.linspace(0.02, 0.09, 1000)
P_exact_grid = np.array([bond_price(FACE_VALUE, COUPON_RATE, MATURITY, y) for y in y_grid])

# 当前收益率附近的久期近似线
y_approx_grid = np.linspace(CURRENT_YIELD - APPROX_SHIFT_RANGE, 
                             CURRENT_YIELD + APPROX_SHIFT_RANGE, 
                             500)
P_approx_grid = P0 * (1 - MD0 * (y_approx_grid - CURRENT_YIELD))

# 截断近似线，使其仅展示在 2% 到 9% 范围内的部分
mask = (y_approx_grid >= 0.02) & (y_approx_grid <= 0.09)
y_approx_plot = y_approx_grid[mask]
P_approx_plot = P_approx_grid[mask]

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(y_grid * 100, P_exact_grid, label='Exact Price-Yield Curve', color='blue', linewidth=2)
plt.plot(y_approx_plot * 100, P_approx_plot, label='Duration-Based Approximation', color='red', linestyle='--', linewidth=2)
plt.axvline(x=CURRENT_YIELD * 100, color='green', linestyle=':', linewidth=1.5, label=f'Current Yield ({CURRENT_YIELD*100:.1f}%)')

plt.title('Bond Price-Yield Curve and Duration Approximation', fontsize=14)
plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.7)

# 保存图表
figure_path = 'price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 封装结果
# ==========================================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 打印输出以便复阅
if __name__ == '__main__':
    print(f"收益率上升100bp后的精确价格: {result['price_at_up100bp']:.4f}")
    print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.4%}")
    print(f"图表已保存至: {result['figure_path']}")
