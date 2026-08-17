import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. 假设处理与参数设定
# ==========================================
# 假设：题目未指明付息频率，采用国内金融学教材默认的每年付息一次（freq=1）
F = 100                  # 面值
coupon_rate = 0.046       # 票息率 4.6%
n_years = 7              # 期限 7年
y_current = 0.053        # 当前收益率 5.3%
freq = 1                 # 年付息频率

# 可调参数：收益率变动幅度（用于久期近似曲线在图上的展示范围，当前设为上下3%）
approx_display_range = 0.03

# ==========================================
# 2. 核心计算函数
# ==========================================
def bond_price(y, F, c, n, freq=1):
    """
    计算债券精确价格（支持标量和数组输入）
    """
    periods = n * freq
    coupon = (c * F) / freq
    y_period = y / freq
    
    # 现值计算公式
    pv_coupons = coupon * (1 - (1 + y_period)**(-periods)) / y_period
    pv_face = F * (1 + y_period)**(-periods)
    return pv_coupons + pv_face

def calc_mod_duration(y, F, c, n, freq=1):
    """
    计算修正久期（支持标量和数组输入）
    """
    periods = n * freq
    coupon = (c * F) / freq
    y_period = y / freq
    
    P = bond_price(y, F, c, n, freq)
    mac_d = 0
    for t in range(1, periods + 1):
        cf = coupon
        if t == periods:
            cf += F
        mac_d += (t / freq) * cf / (1 + y_period)**t
    
    mac_d /= P
    mod_d = mac_d / (1 + y / freq)
    return mod_d

# ==========================================
# 3. 问题求解与计算
# ==========================================
# 当前收益率下的精确价格与修正久期
P_current = bond_price(y_current, F, coupon_rate, n_years, freq)
mod_d_current = calc_mod_duration(y_current, F, coupon_rate, n_years, freq)

# 收益率上升 100 个基点 (1%) 后的计算
delta_y_100bp = 0.01
y_up = y_current + delta_y_100bp
price_at_up100bp = bond_price(y_up, F, coupon_rate, n_years, freq)

# 久期法估计的相对价格变化 (%)
dur_approx_change_up100bp = -mod_d_current * delta_y_100bp

# ==========================================
# 4. 绘制价格-收益率曲线
# ==========================================
# 生成 2% 到 9% 的收益率网格与精确价格
y_grid = np.linspace(0.02, 0.09, 500)
prices_exact = bond_price(y_grid, F, coupon_rate, n_years, freq)

# 在当前收益率附近生成基于久期的近似价格线
y_approx_min = max(0.02, y_current - approx_display_range)
y_approx_max = min(0.09, y_current + approx_display_range)
y_approx = np.linspace(y_approx_min, y_approx_max, 100)
# 久期一阶近似: P(y) ≈ P(y0) * [1 - ModD * (y - y0)]
prices_approx = P_current * (1 - mod_d_current * (y_approx - y_current))

# 设置中文字体与绘图风格
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 6))

# 绘制精确曲线与近似曲线
ax.plot(y_grid * 100, prices_exact, label='精确价格-收益率曲线', color='blue', linewidth=2.5)
ax.plot(y_approx * 100, prices_approx, label='基于久期的一阶近似', color='red', linestyle='--', linewidth=2)

# 标注当前收益率所在点
ax.scatter([y_current * 100], [P_current], color='black', s=60, zorder=5)
ax.annotate(f'当前 (y={y_current*100:.1f}%, P={P_current:.2f})', 
            xy=(y_current*100, P_current), xytext=(20, 20),
            textcoords='offset points', arrowprops=dict(arrowstyle='->', color='black'))

# 标注上升 100bp 后的精确点
ax.scatter([y_up * 100], [price_at_up100bp], color='green', s=60, zorder=5)
ax.annotate(f'+100bp (y={y_up*100:.1f}%, P={price_at_up100bp:.2f})', 
            xy=(y_up*100, price_at_up100bp), xytext=(20, -30),
            textcoords='offset points', arrowprops=dict(arrowstyle='->', color='green'))

ax.set_title('债券价格-收益率曲线及久期近似', fontsize=16)
ax.set_xlabel('收益率 (%)', fontsize=12)
ax.set_ylabel('债券价格', fontsize=12)
ax.legend(fontsize=12)
ax.grid(True, linestyle=':', alpha=0.6)

# 保存图形
figure_path = 'price_yield_curve.png'
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 5. 填充结果字典
# ==========================================
result = {
    'price_at_up100bp': round(price_at_up100bp, 6),
    'dur_approx_change_up100bp': round(dur_approx_change_up100bp, 6),
    'figure_path': figure_path
}

# 打印结果以供验证 (课堂投屏可直观展示)
print("=== 计算结果 ===")
print(f"收益率上升100bp后的精确价格: {result['price_at_up100bp']}")
print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp'] * 100:.4f}%")
print(f"图形已保存至: {result['figure_path']}")
