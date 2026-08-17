import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 债券参数设置
# ==========================================
face_value = 100.0
coupon_rate = 0.046
maturity = 7
current_yield = 0.053
annual_coupon = face_value * coupon_rate

# 收益率变动幅度（可调参数）：控制久期近似曲线的绘制范围（当前收益率上下各浮动该幅度）
yield_change_amplitude = 0.02  # 例如 2% (200个基点)

# ==========================================
# 核心计算函数
# ==========================================
def calculate_bond_price(yields, C, F, T):
    """
    计算债券的精确价格（支持向量化）
    yields: 收益率数组或标量
    C: 票息
    F: 面值
    T: 期限
    """
    yields = np.asarray(yields).reshape(-1, 1)
    t = np.arange(1, T + 1).reshape(1, -1)
    pv_coupons = np.sum(C / (1 + yields) ** t, axis=1)
    pv_face = F / (1 + yields.squeeze()) ** T
    return pv_coupons + pv_face

def calculate_modified_duration(yield_val, C, F, T):
    """
    计算修正久期
    """
    t = np.arange(1, T + 1)
    price = calculate_bond_price(yield_val, C, F, T).item()
    pv_cf = C / (1 + yield_val) ** t
    pv_face = F / (1 + yield_val) ** T
    macaulay_duration = (np.sum(t * pv_cf) + T * pv_face) / price
    modified_duration = macaulay_duration / (1 + yield_val)
    return modified_duration, price

# ==========================================
# 计算当前收益率下的久期与价格
# ==========================================
mod_dur, price_at_current = calculate_modified_duration(current_yield, annual_coupon, face_value, maturity)

# ==========================================
# 计算 100 个基点上升后的精确价格与久期法相对变化
# ==========================================
yield_up_100bp = current_yield + 0.01
price_at_up100bp = calculate_bond_price(yield_up_100bp, annual_coupon, face_value, maturity).item()

# 久期法估计的相对价格变化: ΔP/P ≈ -Mod_Dur * Δy
dur_approx_change_up100bp = -mod_dur * 0.01

# ==========================================
# 绘制价格-收益率曲线与久期近似
# ==========================================
# 1. 生成精确曲线的收益率范围 (2% ~ 9%)
yields_full = np.linspace(0.02, 0.09, 500)
prices_exact_full = calculate_bond_price(yields_full, annual_coupon, face_value, maturity)

# 2. 生成本地久期近似曲线的收益率范围
yields_local = np.linspace(current_yield - yield_change_amplitude, 
                           current_yield + yield_change_amplitude, 200)
# 久期近似公式: P(y) ≈ P(y0) * [1 - Mod_Dur * (y - y0)]
prices_dur_approx = price_at_current * (1 - mod_dur * (yields_local - current_yield))

# 画图设置
plt.figure(figsize=(10, 6))
plt.plot(yields_full * 100, prices_exact_full, 'b-', linewidth=2, label='Exact Price-Yield Curve')
plt.plot(yields_local * 100, prices_dur_approx, 'r--', linewidth=2, label='Duration-based Approximation')

# 标注当前收益率点
plt.scatter(current_yield * 100, price_at_current, color='black', zorder=5)
plt.annotate(f'Current Yield ({current_yield*100:.1f}%)\nPrice: {price_at_current:.2f}',
             xy=(current_yield * 100, price_at_current),
             xytext=(current_yield * 100 + 0.5, price_at_current + 4),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5),
             fontsize=10)

plt.title('Bond Price-Yield Curve and Duration Approximation', fontsize=14)
plt.xlabel('Yield (%)', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle=':', alpha=0.7)

# 保存图像
figure_path = 'price_yield_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==========================================
# 构建输出契约字典
# ==========================================
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 打印结果以便验证
print(f"当前收益率下的精确价格: {price_at_current:.4f}")
print(f"修正久期: {mod_dur:.4f}")
print(f"收益率上升100bp后的精确价格: {result['price_at_up100bp']:.4f}")
print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.4%}")
print(f"图像已保存至: {result['figure_path']}")
