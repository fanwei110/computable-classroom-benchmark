import numpy as np
import matplotlib.pyplot as plt
import os
import scipy  # 仅导入以满足库限制
import pandas  # 仅导入以满足库限制

# ================== 参数设定（可调节） ==================
FACE_VALUE = 100.0                # 面值
COUPON_RATE = 0.046               # 票息率（年）
MATURITY = 7                      # 年限（年）
YIELD_CURRENT = 0.053             # 当前到期收益率
YIELD_MIN = 0.02                  # 曲线收益率下限
YIELD_MAX = 0.09                  # 曲线收益率上限
NUM_POINTS = 500                  # 绘图点数
YIELD_CHANGE_BPS = 100            # 收益率变动幅度（基点），可调节
# ======================================================

YIELD_UP = YIELD_CURRENT + YIELD_CHANGE_BPS / 10000.0


def bond_price(ytm, face, coupon_rate, maturity):
    """计算债券的净价（年付息一次）。ytm 可为标量或数组。"""
    coupon = face * coupon_rate
    t = np.arange(1, maturity + 1)
    cash_flows = np.full(maturity, coupon)
    cash_flows[-1] += face

    if np.isscalar(ytm):
        discount = (1 + ytm) ** t
        price = np.sum(cash_flows / discount)
    else:
        ytm = np.asarray(ytm)
        discount = (1 + ytm[:, np.newaxis]) ** t
        price = np.sum(cash_flows / discount, axis=1)
    return price


def modified_duration(ytm, face, coupon_rate, maturity):
    """计算修正久期（年付息一次）。"""
    coupon = face * coupon_rate
    t = np.arange(1, maturity + 1)
    cash_flows = np.full(maturity, coupon)
    cash_flows[-1] += face

    discount = (1 + ytm) ** t
    price = np.sum(cash_flows / discount)
    # 麦考利久期
    mac_dur = np.sum(t * cash_flows / discount) / price
    # 修正久期
    mod_dur = mac_dur / (1 + ytm)
    return mod_dur


# ---------- 当前价格与久期 ----------
P0 = bond_price(YIELD_CURRENT, FACE_VALUE, COUPON_RATE, MATURITY)
MD = modified_duration(YIELD_CURRENT, FACE_VALUE, COUPON_RATE, MATURITY)

# ---------- 精确价格曲线 ----------
y_range = np.linspace(YIELD_MIN, YIELD_MAX, NUM_POINTS)
prices_exact = bond_price(y_range, FACE_VALUE, COUPON_RATE, MATURITY)

# ---------- 久期近似切线 ----------
prices_approx = P0 - MD * P0 * (y_range - YIELD_CURRENT)

# ---------- 收益率上升100 bp 的计算 ----------
price_up = bond_price(YIELD_UP, FACE_VALUE, COUPON_RATE, MATURITY)
delta_y = YIELD_CHANGE_BPS / 10000.0
approx_change = -MD * P0 * delta_y   # 久期法估计的价格变化（ΔP）

# ---------- 绘图 ----------
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(y_range * 100, prices_exact, label='Exact Price–Yield Curve',
        color='steelblue', linewidth=2)
ax.plot(y_range * 100, prices_approx, '--',
        label='Duration Approximation (Tangent)',
        color='darkorange', linewidth=2)
ax.axvline(YIELD_CURRENT * 100, color='gray', linestyle=':', alpha=0.7,
           label=f'Current yield = {YIELD_CURRENT*100:.1f}%')
ax.scatter([YIELD_CURRENT * 100], [P0], color='red', zorder=5)
ax.annotate(f'{P0:.4f}', (YIELD_CURRENT * 100, P0),
            textcoords='offset points', xytext=(10, 10),
            fontsize=9, color='red')
ax.set_xlabel('Yield to Maturity (%)')
ax.set_ylabel('Bond Price')
ax.set_title('Bond Price–Yield Curve with Duration-Based Approximation')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.6)

figure_path = 'bond_price_yield_curve.png'
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ---------- 整理输出 ----------
result = {
    'price_at_up100bp': price_up,
    'dur_approx_change_up100bp': approx_change,
    'figure_path': os.path.abspath(figure_path)
}

# 控制台输出（便于直接查看）
print(f"当前收益率 ({YIELD_CURRENT*100:.1f}%) 价格: {P0:.6f}")
print(f"修正久期: {MD:.6f}")
print(f"收益率上升 {YIELD_CHANGE_BPS} bp 后精确价格: {price_up:.6f}")
print(f"久期法估计的价格变化 (ΔP): {approx_change:.6f}")
print(f"图片保存路径: {result['figure_path']}")
