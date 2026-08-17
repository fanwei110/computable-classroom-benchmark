import numpy as np
import matplotlib.pyplot as plt

# ==============================================================
# 可调参数
# ==============================================================
FACE_VALUE = 100.0          # 面值
COUPON_RATE = 0.046         # 票息率（年化）
MATURITY = 7                # 期限（年）
YIELD_CURRENT = 0.053       # 当前到期收益率
DELTA_Y_BP = 100            # 收益率变动幅度，单位：基点
YIELD_SHOCK = DELTA_Y_BP / 10000.0  # 转换为小数（100 bp = 0.01）

# 假设：每年付息一次（若需半年付息，可调整频率，内部保持一致）
FREQ = 1                    # 年付息次数

# ==============================================================
# 现金流生成
# ==============================================================
periods = np.arange(1, MATURITY * FREQ + 1)  # 1, 2, ..., 7
coupon_pmt = FACE_VALUE * COUPON_RATE / FREQ
cashflows = np.full_like(periods, coupon_pmt, dtype=float)
cashflows[-1] += FACE_VALUE   # 最后一期加入面值

# ==============================================================
# 定价函数（给定到期收益率，返回价格）
# ==============================================================
def bond_price(ytm):
    """计算债券精确价格，ytm为年化收益率（小数），假设年付息FREQ=1。"""
    # 如果FREQ>1，需要调整贴现期数和每期收益率；此处FREQ=1简化
    discount_factors = (1 + ytm) ** (-periods)   # 年付息
    return np.sum(cashflows * discount_factors)

# ==============================================================
# 久期计算（麦考利久期和修正久期）
# ==============================================================
def bond_duration(ytm):
    """返回麦考利久期和修正久期。"""
    price = bond_price(ytm)
    disc = (1 + ytm) ** (-periods)
    pv_cf = cashflows * disc
    mac_dur = np.sum(periods * pv_cf) / price / FREQ   # 以年为单位
    mod_dur = mac_dur / (1 + ytm / FREQ)
    return mac_dur, mod_dur

# ==============================================================
# 当前收益率下的基准价格与久期
# ==============================================================
P0 = bond_price(YIELD_CURRENT)
mac_dur0, mod_dur0 = bond_duration(YIELD_CURRENT)

# 收益率上升100个基点后的精确价格
YIELD_UP = YIELD_CURRENT + YIELD_SHOCK
P_up = bond_price(YIELD_UP)

# 久期法估计的相对价格变化（ΔP/P ≈ -D_mod × Δy）
dur_approx_rel_change = -mod_dur0 * YIELD_SHOCK

# ==============================================================
# 价格-收益率曲线数据
# ==============================================================
YIELD_GRID = np.linspace(0.02, 0.09, 500)  # 2% 到 9%
price_exact = np.array([bond_price(y) for y in YIELD_GRID])

# 基于久期的线性近似（在当前收益率点上的切线）
price_dur_approx = P0 - mod_dur0 * P0 * (YIELD_GRID - YIELD_CURRENT)

# ==============================================================
# 绘图
# ==============================================================
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(YIELD_GRID * 100, price_exact, label='Precise price-yield curve', linewidth=2)
ax.plot(YIELD_GRID * 100, price_dur_approx, '--', label='Duration-based approximation', linewidth=2)
ax.axvline(YIELD_CURRENT * 100, color='gray', linestyle=':', alpha=0.7, label=f'Current yield ({YIELD_CURRENT*100:.1f}%)')
ax.axvline(YIELD_UP * 100, color='red', linestyle=':', alpha=0.7, label=f'Yield +{DELTA_Y_BP}bp ({YIELD_UP*100:.2f}%)')
ax.set_xlabel('Yield to Maturity (%)')
ax.set_ylabel('Bond Price')
ax.set_title('Price–Yield Curve with Duration Approximation')
ax.legend()
ax.grid(True, alpha=0.3)

# 保存图像
FIG_PATH = 'bond_price_yield_curve.png'
fig.savefig(FIG_PATH, dpi=150, bbox_inches='tight')
plt.close(fig)

# ==============================================================
# 汇总结果
# ==============================================================
result = {
    'price_at_up100bp': round(P_up, 6),
    'dur_approx_change_up100bp': round(dur_approx_rel_change, 6),
    'figure_path': FIG_PATH
}

# 运行时打印结果以便查验
if __name__ == '__main__':
    print('=== 债券定价与久期分析结果 ===')
    print(f'当前收益率: {YIELD_CURRENT*100:.2f}%')
    print(f'当前价格: {P0:.6f}')
    print(f'麦考利久期: {mac_dur0:.4f} 年')
    print(f'修正久期: {mod_dur0:.4f}')
    print(f'收益率上升 {DELTA_Y_BP} bp 后的精确价格: {P_up:.6f}')
    print(f'久期法估计的相对价格变化: {dur_approx_rel_change:.6f} ({dur_approx_rel_change*100:.4f}%)')
    print(f'图形已保存至: {FIG_PATH}')
    print('\n输出字典 result:')
    print(result)
