import numpy as np
import matplotlib.pyplot as plt

# ========== 可调参数 ==========
FACE = 100.0             # 面值
COUPON_RATE = 0.046      # 票面利率（年化）
MATURITY = 7             # 剩余期限（年）
YIELD_CURRENT = 0.053    # 当前到期收益率
YIELD_SHIFT = 0.01       # 收益率变动幅度（可调，此处为+100bp）

# ========== 辅助函数 ==========
def bond_price(ytm, cpn_rate, face, n):
    """计算债券价格（假设每年付息一次，到期还本）"""
    pv = 0.0
    coupon = face * cpn_rate
    for t in range(1, n + 1):
        cf = coupon + (face if t == n else 0.0)
        pv += cf / (1.0 + ytm) ** t
    return pv

def bond_duration(ytm, cpn_rate, face, n):
    """返回 (麦考利久期, 修正久期)"""
    p = bond_price(ytm, cpn_rate, face, n)
    coupon = face * cpn_rate
    weighted = 0.0
    for t in range(1, n + 1):
        cf = coupon + (face if t == n else 0.0)
        weighted += t * cf / (1.0 + ytm) ** t
    mac_dur = weighted / p
    mod_dur = mac_dur / (1.0 + ytm)
    return mac_dur, mod_dur

# ========== 1. 收益率网格上的精确定价 ==========
YIELD_MIN = 0.02
YIELD_MAX = 0.09
y_grid = np.linspace(YIELD_MIN, YIELD_MAX, 400)   # 足够平滑的曲线
price_exact = np.array([bond_price(y, COUPON_RATE, FACE, MATURITY) for y in y_grid])

# ========== 2. 当前收益率处的价格及久期 ==========
price_current = bond_price(YIELD_CURRENT, COUPON_RATE, FACE, MATURITY)
mac_dur, mod_dur = bond_duration(YIELD_CURRENT, COUPON_RATE, FACE, MATURITY)

# 基于久期的价格近似（切线） P(y) ≈ P(y0) * [1 - 修正久期 * (y - y0)]
price_approx = price_current * (1.0 - mod_dur * (y_grid - YIELD_CURRENT))

# ========== 3. +100bp 情况 ==========
y_up = YIELD_CURRENT + YIELD_SHIFT
price_up100 = bond_price(y_up, COUPON_RATE, FACE, MATURITY)              # 精确价格
dur_approx_change_up100bp = -mod_dur * YIELD_SHIFT                      # 久期近似的相对价格变化

# ========== 4. 画图并保存 ==========
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(y_grid * 100, price_exact, label='精确价格', linewidth=1.8)
ax.plot(y_grid * 100, price_approx, '--', label='久期近似 (切线)', linewidth=1.5)
ax.axvline(YIELD_CURRENT * 100, color='gray', linestyle=':', label=f'当前收益率 {YIELD_CURRENT*100:.2f}%')
ax.set_xlabel('到期收益率 (%)')
ax.set_ylabel('债券价格')
ax.set_title('债券价格—收益率曲线 (面值100, 票息4.6%, 7年期)')
ax.legend()
ax.grid(True, alpha=0.4)
fig.tight_layout()

figure_filename = 'price_yield_curve.png'
fig.savefig(figure_filename, dpi=150)
plt.close(fig)   # 避免在无图形界面环境下弹出窗口

# ========== 输出结果字典 ==========
result = {
    'price_at_up100bp': price_up100,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': figure_filename
}

# 课堂运行时可直接打印查验
print(result)
