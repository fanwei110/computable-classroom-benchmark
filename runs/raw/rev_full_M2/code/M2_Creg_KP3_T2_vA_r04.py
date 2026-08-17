import os
import numpy as np
import matplotlib.pyplot as plt
import scipy  # 满足要求，即使不直接使用
import pandas as pd  # 满足要求

# ============================================================
# 可调参数
# ============================================================
YIELD_SHIFT_BPS = 100  # 收益率变动幅度（基点），可调

# 债券基本信息
FACE = 100.0
COUPON_RATE = 0.046
MATURITY = 7          # 年
YIELD_CURRENT = 0.053 # 当前收益率
FREQ = 1              # 每年付息次数（年付息）

# ============================================================
# 价格与敏感性计算函数
# ============================================================
def bond_price(ytm, face, coupon_rate, maturity, freq=1):
    """计算债券全价（年付息频率可调，此处 freq=1）"""
    # 每期票息
    coupon = face * coupon_rate / freq
    # 付息期数
    periods = maturity * freq
    # 时间点（年）
    times = np.arange(1, periods + 1) / freq
    cashflows = np.full(periods, coupon)
    # 最后一期还本
    cashflows[-1] += face
    # 每期折现因子，注意收益率需根据频率调整
    discount = (1 + ytm / freq) ** (times * freq)  # 等价于 (1 + ytm)**times 当 freq=1
    pv = np.sum(cashflows / discount)
    return pv

def bond_price_derivative(ytm, face, coupon_rate, maturity, freq=1):
    """计算债券价格对收益率的一阶导数（dP/dy）"""
    coupon = face * coupon_rate / freq
    periods = maturity * freq
    times = np.arange(1, periods + 1) / freq
    cashflows = np.full(periods, coupon)
    cashflows[-1] += face
    # 解析导数
    discount = (1 + ytm / freq) ** (times * freq)
    deriv_factor = -times / (1 + ytm / freq)
    deriv = np.sum(cashflows * deriv_factor / discount)
    return deriv

# ============================================================
# 计算精确价格-收益率曲线
# ============================================================
yields = np.linspace(0.02, 0.09, 500)
prices_exact = np.array([bond_price(y, FACE, COUPON_RATE, MATURITY, FREQ) for y in yields])

# 当前收益率下的价格与导数
P0 = bond_price(YIELD_CURRENT, FACE, COUPON_RATE, MATURITY, FREQ)
deriv0 = bond_price_derivative(YIELD_CURRENT, FACE, COUPON_RATE, MATURITY, FREQ)

# 基于久期的切线近似：P_approx(y) = P0 + deriv0 * (y - y0)
prices_approx = P0 + deriv0 * (yields - YIELD_CURRENT)

# ============================================================
# 绘图
# ============================================================
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(yields * 100, prices_exact, label='Exact Price', linewidth=1.5)
ax.plot(yields * 100, prices_approx, '--', label='Duration Approximation', linewidth=1.5)
ax.axvline(YIELD_CURRENT * 100, color='gray', linestyle=':', alpha=0.7,
           label=f'Current Yield ({YIELD_CURRENT*100:.1f}%)')
ax.set_xlabel('Yield (%)')
ax.set_ylabel('Price')
ax.set_title('Bond Price–Yield Curve')
ax.legend()
ax.grid(True)
figure_path = os.path.abspath('bond_price_curve.png')
fig.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close(fig)

# ============================================================
# 收益率上升指定基点后的精确价格及久期近似相对变化
# ============================================================
dy = YIELD_SHIFT_BPS / 10_000.0   # 基点转小数
y_up = YIELD_CURRENT + dy
price_up_exact = bond_price(y_up, FACE, COUPON_RATE, MATURITY, FREQ)

# 修正久期
D_mod = -deriv0 / P0
# 久期近似得到的相对价格变化（小数）
rel_change_approx = -D_mod * dy

# ============================================================
# 输出字典
# ============================================================
result = {
    'price_at_up100bp': price_up_exact,
    'dur_approx_change_up100bp': rel_change_approx,
    'figure_path': figure_path
}

# 可选控制台输出，便于查看
if __name__ == '__main__':
    print('Result dictionary:')
    for k, v in result.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.6f}")
        else:
            print(f"  {k}: {v}")
