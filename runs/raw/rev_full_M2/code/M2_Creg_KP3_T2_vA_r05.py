import numpy as np
import matplotlib.pyplot as plt
import os

# ==================== 可调参数 ====================
FACE = 100.0           # 面值
COUPON_RATE = 0.046    # 票息率（年化）
MATURITY = 7           # 年限
FREQ = 1               # 付息频率（1 = 年付）
YIELD_CURRENT = 0.053  # 当前收益率
YIELD_MIN = 0.02       # 曲线起点
YIELD_MAX = 0.09       # 曲线终点
DELTA_Y = 0.01         # 收益率变动幅度（可调，默认100个基点）
FIG_FILENAME = "bond_price_yield.png"

# ==================== 债券定价函数 ====================
def bond_price(ytm, coupon_rate, face, maturity, freq=1):
    """精确债券价格（年/半年复利）"""
    coupon = coupon_rate * face / freq
    periods = maturity * freq
    t = np.arange(1, periods + 1)
    cashflows = np.full(periods, coupon)
    cashflows[-1] += face
    discount = (1 + ytm / freq) ** t
    return np.sum(cashflows / discount)

# ==================== 久期计算函数 ====================
def bond_duration(ytm, coupon_rate, face, maturity, freq=1):
    """计算麦考利久期（年）和修正久期"""
    coupon = coupon_rate * face / freq
    periods = maturity * freq
    t = np.arange(1, periods + 1)
    cashflows = np.full(periods, coupon)
    cashflows[-1] += face
    y_per = ytm / freq
    discount = (1 + y_per) ** t
    pv = cashflows / discount
    price = np.sum(pv)
    mac_dur_periods = np.sum(t * pv) / price
    mac_dur_years = mac_dur_periods / freq
    mod_dur = mac_dur_years / (1 + y_per)
    return mac_dur_years, mod_dur

# ==================== 主计算 ====================
P0 = bond_price(YIELD_CURRENT, COUPON_RATE, FACE, MATURITY, FREQ)
mac_dur, mod_dur = bond_duration(YIELD_CURRENT, COUPON_RATE, FACE, MATURITY, FREQ)

# 收益率上升 DELTA_Y 后的精确价格与相对变化
y_up = YIELD_CURRENT + DELTA_Y
price_up = bond_price(y_up, COUPON_RATE, FACE, MATURITY, FREQ)
exact_change = (price_up - P0) / P0   # 精确相对变化（备用）
approx_change = -mod_dur * DELTA_Y    # 久期近似相对变化

# ==================== 画图 ====================
yields = np.linspace(YIELD_MIN, YIELD_MAX, 500)
prices_exact = np.array([bond_price(y, COUPON_RATE, FACE, MATURITY, FREQ) for y in yields])
prices_tangent = P0 - mod_dur * P0 * (yields - YIELD_CURRENT)   # 切线（久期近似）

plt.figure(figsize=(8, 6))
plt.plot(yields, prices_exact, label="Exact Price", color="blue")
plt.plot(yields, prices_tangent, label="Duration Approximation", color="red", linestyle="--")
plt.axvline(YIELD_CURRENT, color="gray", linestyle=":", alpha=0.7)
plt.axhline(P0, color="gray", linestyle=":", alpha=0.7)
plt.xlabel("Yield")
plt.ylabel("Price")
plt.title("Bond Price vs Yield")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

fig_path = os.path.abspath(FIG_FILENAME)
plt.savefig(fig_path, dpi=150)
plt.close()

# ==================== 结果输出 ====================
result = {
    "price_at_up100bp": price_up,
    "dur_approx_change_up100bp": approx_change,
    "figure_path": fig_path,
}

if __name__ == "__main__":
    # 直接运行时输出结果，便于核查
    print(result)
