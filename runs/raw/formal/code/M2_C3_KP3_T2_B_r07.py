import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------- 参数 -------------
face_value = 100
coupon_rate = 0.046
coupon = face_value * coupon_rate
T = 7
YTM0 = 0.053
dy = 0.01  # +100bp

# 收益率范围
yields = np.linspace(0.02, 0.09, 100)

# ------------- 价格计算函数 -------------
def bond_price(ytm):
    t = np.arange(1, T+1)
    pv_coupons = np.sum(coupon / (1+ytm)**t)
    pv_face = face_value / (1+ytm)**T
    return pv_coupons + pv_face

def macaulay_duration(ytm):
    t = np.arange(1, T+1)
    pv_cf = coupon / (1+ytm)**t
    pv_face = face_value / (1+ytm)**T
    pv_total = np.sum(pv_cf) + pv_face
    duration = (np.sum(t * pv_cf) + T * pv_face) / pv_total
    return duration

# ------------- 精确价格与久期近似 -------------
P0 = bond_price(YTM0)
mac_dur = macaulay_duration(YTM0)
mod_dur = mac_dur / (1 + YTM0)

P_up = bond_price(YTM0 + dy)
P_down = bond_price(YTM0 - dy)

# 精确相对变化（%）：
exact_change_up = (P_up - P0) / P0 * 100
dur_approx_change_up = -mod_dur * dy * 100  # 百分比

# 作图
prices_exact = [bond_price(y) for y in yields]
dur_approx_price = [P0 * (1 - mod_dur*(y - YTM0)) for y in yields]

plt.figure(figsize=(10,6))
plt.plot(yields*100, prices_exact, label='Exact Price', linewidth=2)
plt.plot(yields*100, dur_approx_price, '--', label='Duration Approximation', linewidth=2)
plt.xlabel('Yield to Maturity (%)')
plt.ylabel('Price')
plt.title('Price-Yield Curve & Duration Approximation')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('price_yield_duration.png')
plt.close()

# 结果汇总
result = {
    'price_at_up100bp': round(P_up, 4),
    'dur_approx_change_up100bp': round(dur_approx_change_up, 4),
    'figure_path': 'price_yield_duration.png'
}

print(result)
