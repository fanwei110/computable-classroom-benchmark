import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 债券参数与假设设定
# ==========================================
# 假设：本题未指明付息频率，按国内《证券投资学》常规惯例，采用按年付息
face_value = 100.0        # 面值
coupon_rate = 0.046       # 票息率
maturity = 7              # 期限（年）
current_yield = 0.053     # 当前收益率

# 可调：收益率变动幅度（用于特定场景计算与图表标注），此处为100个基点
delta_y = 0.01            

# ==========================================
# 核心函数定义
# ==========================================
def bond_price(ytm, face_value, coupon_rate, maturity):
    """
    计算债券精确价格：现金流贴现之和
    """
    periods = np.arange(1, maturity + 1)
    coupon = face_value * coupon_rate
    # 票息贴现
    pv_coupons = np.sum(coupon / (1 + ytm) ** periods)
    # 面值贴现
    pv_face = face_value / (1 + ytm) ** maturity
    return pv_coupons + pv_face

def modified_duration(ytm, face_value, coupon_rate, maturity):
    """
    计算修正久期：价格对收益率变动的线性敏感性
    """
    periods = np.arange(1, maturity + 1)
    coupon = face_value * coupon_rate
    price = bond_price(ytm, face_value, coupon_rate, maturity)
    
    # 各期现金流
    cash_flows = np.full(maturity, coupon)
    cash_flows[-1] += face_value
    
    # Macaulay久期
    pv_cf = cash_flows / (1 + ytm) ** periods
    mac_duration = np.sum(periods * pv_cf) / price
    
    # 修正久期
    mod_duration = mac_duration / (1 + ytm)
    return mod_duration

# ==========================================
# 1. 在 2% 到 9% 的收益率网格上为精确曲线定价
# ==========================================
y_grid = np.linspace(0.02, 0.09, 700)
p_exact_grid = np.array([bond_price(y, face_value, coupon_rate, maturity) for y in y_grid])

# ==========================================
# 2. 在 5.3% 附近叠加基于久期的近似
# ==========================================
# 计算当前收益率下的精确价格和修正久期
p_at_y0 = bond_price(current_yield, face_value, coupon_rate, maturity)
mod_dur_y0 = modified_duration(current_yield, face_value, coupon_rate, maturity)

# 久期的一阶线性近似: P(y) ≈ P(y0) - P(y0) * ModDur * (y - y0)
p_duration_approx_grid = p_at_y0 - p_at_y0 * mod_dur_y0 * (y_grid - current_yield)

# ==========================================
# 3. 报告 +100bp 的精确价格与久期法估计的相对变化
# ==========================================
y_up_100bp = current_yield + delta_y
price_at_up100bp = bond_price(y_up_100bp, face_value, coupon_rate, maturity)

# 久期法估计的相对价格变化: ΔP/P ≈ -ModDur * Δy
dur_approx_change_up100bp = -mod_dur_y0 * delta_y

# ==========================================
# 4. 绘图与保存
# ==========================================
plt.figure(figsize=(10, 6))

# 绘制精确价格-收益率曲线
plt.plot(y_grid * 100, p_exact_grid, label='Exact Price-Yield Curve', color='blue', linewidth=2)

# 绘制久期近似线
plt.plot(y_grid * 100, p_duration_approx_grid, label='Duration-based Approximation', 
         color='red', linestyle='--', linewidth=2)

# 标注当前收益率点
plt.scatter([current_yield * 100], [p_at_y0], color='black', zorder=5, label=f'Current Yield ({current_yield*100:.1f}%)')

# 标注 +100bp 变动幅度对应的精确点与近似点差异(可视化可调幅度 delta_y)
y_up_point = current_yield + delta_y
p_exact_up = bond_price(y_up_point, face_value, coupon_rate, maturity)
p_approx_up = p_at_y0 * (1 - mod_dur_y0 * delta_y)
plt.scatter([y_up_point * 100], [p_exact_up], color='green', zorder=5, marker='v', label=f'Exact Price at +{delta_y*100:.0f}bp')
plt.scatter([y_up_point * 100], [p_approx_up], color='orange', zorder=5, marker='^', label=f'Approx Price at +{delta_y*100:.0f}bp')

# 图表美化
plt.title('Bond Price-Yield Curve and Duration Approximation', fontsize=14)
plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.legend(fontsize=10)
plt.grid(True, linestyle=':', alpha=0.7)

# 保存图形
figure_path = 'price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 输出契约：填充 result 字典
# ==========================================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 课堂投屏打印验证 (不改变result内容，仅供展示)
if __name__ == '__main__':
    print("--- 计算结果 ---")
    print(f"当前收益率下的精确价格: {p_at_y0:.4f}")
    print(f"修正久期: {mod_dur_y0:.4f}")
    print(f"收益率上升100bp后的精确价格: {result['price_at_up100bp']:.4f}")
    print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.4%}")
    print(f"图形已保存至: {result['figure_path']}")
