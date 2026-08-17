import numpy as np
import matplotlib.pyplot as plt

# ==================== 债券参数设定 ====================
face_value = 100           # 面值
coupon_rate = 0.046        # 票息率 4.6%
years_to_maturity = 7      # 期限 7 年
current_yield = 0.053      # 当前收益率 5.3%
yield_step = 0.001         # 收益率变动幅度（可调参数，控制曲线绘制的离散精度）

# ==================== 核心计算函数 ====================
def bond_price(face_value, coupon_rate, years_to_maturity, y):
    """
    计算债券精确价格
    y 可以是标量或 numpy 数组
    """
    y = np.asarray(y)
    C = face_value * coupon_rate
    t = np.arange(1, years_to_maturity + 1).reshape(-1, 1) # (T, 1)
    
    # 处理标量和数组情况，统一升维以便广播
    if y.ndim == 0:
        y = y.reshape(1)
    y = y.reshape(1, -1) # (1, N)
    
    pv_coupons = np.sum(C / (1 + y)**t, axis=0)
    pv_face = face_value / (1 + y)**years_to_maturity
    return pv_coupons + pv_face

def bond_modified_duration(face_value, coupon_rate, years_to_maturity, y):
    """
    计算修正久期 (Modified Duration)
    """
    C = face_value * coupon_rate
    P = bond_price(face_value, coupon_rate, years_to_maturity, y)
    t = np.arange(1, years_to_maturity + 1)
    
    # Macaulay 久期
    mac_duration = np.sum(t * C / (1 + y)**t) + years_to_maturity * face_value / (1 + y)**years_to_maturity
    mac_duration /= P
    
    # 修正久期
    mod_duration = mac_duration / (1 + y)
    return mod_duration

# ==================== 计算当前指标 ====================
P0 = bond_price(face_value, coupon_rate, years_to_maturity, current_yield)
D_mod = bond_modified_duration(face_value, coupon_rate, years_to_maturity, current_yield)

# ==================== 收益率上升 100bp 后的指标计算 ====================
yield_up_100bp = current_yield + 0.01  # 上升 100 个基点 (1%)
price_at_up100bp = bond_price(face_value, coupon_rate, years_to_maturity, yield_up_100bp)
dur_approx_change_up100bp = -D_mod * 0.01  # 久期法估计的相对价格变化 ΔP/P ≈ -D_mod * Δy

# ==================== 生成价格-收益率曲线数据 ====================
y_range = np.arange(0.02, 0.09 + yield_step, yield_step)
prices_exact = bond_price(face_value, coupon_rate, years_to_maturity, y_range)
# 久期近似：P_approx(y) = P0 + dP/dy * (y - y0) = P0 - P0 * D_mod * (y - y0)
prices_approx = P0 - P0 * D_mod * (y_range - current_yield)

# ==================== 绘图 ====================
plt.figure(figsize=(10, 6))
plt.plot(y_range * 100, prices_exact, label='Exact Price-Yield Curve', color='blue', linewidth=2)
plt.plot(y_range * 100, prices_approx, label='Duration-based Approximation', color='red', linestyle='--', linewidth=2)

# 标注当前收益率位置
plt.axvline(x=current_yield * 100, color='green', linestyle=':', linewidth=1.5, label=f'Current Yield ({current_yield*100:.1f}%)')
plt.scatter([current_yield * 100], [P0], color='black', zorder=5)

plt.title('Price-Yield Curve and Duration Approximation', fontsize=14)
plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)

figure_path = 'price_yield_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# ==================== 结果存入字典 ====================
result = {
    'price_at_up100bp': price_at_up100bp.item() if isinstance(price_at_up100bp, np.ndarray) else price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp.item() if isinstance(dur_approx_change_up100bp, np.ndarray) else dur_approx_change_up100bp,
    'figure_path': figure_path
}

# 打印结果供查阅
print("=== Result Dictionary ===")
for k, v in result.items():
    if isinstance(v, float):
        print(f"{k}: {v:.6f}")
    else:
        print(f"{k}: {v}")
