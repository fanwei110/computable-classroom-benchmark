import numpy as np
import matplotlib.pyplot as plt

# 债券参数
face_value = 100.0
coupon_rate = 4.6          # 票息（%）
coupon = coupon_rate       # 年付息额
nper = 7                   # 剩余年限
ytm_current = 5.3 / 100.0  # 当前到期收益率

# 可选：收益率变动范围（可调）
y_min = 0.02   # 2%
y_max = 0.09   # 9%
delta_y_bp = 100  # bp 变动幅度（可调）
delta_y = delta_y_bp / 10000.0  # 转换为小数

def bond_price(ytm):
    """计算债券的精确价格（年付息）"""
    pv_coupons = sum(coupon / (1 + ytm) ** t for t in range(1, nper + 1))
    pv_face = face_value / (1 + ytm) ** nper
    return pv_coupons + pv_face

# 当前价格与修正久期
P0 = bond_price(ytm_current)

# 麦考利久期
pv_flows = [coupon / (1 + ytm_current) ** t for t in range(1, nper)]
pv_flows.append((coupon + face_value) / (1 + ytm_current) ** nper)
mac_dur = sum((t + 1) * pv_flows[t] for t in range(nper)) / P0
mod_dur = mac_dur / (1 + ytm_current)   # 修正久期

# 收益率增加100 bp后的精确价格
y_new = ytm_current + delta_y
P_new = bond_price(y_new)

# 久期法估计的相对价格变化和近似价格
dur_approx_relative_change = -mod_dur * delta_y   # ΔP / P
dur_approx_absolute_change = P0 * dur_approx_relative_change

# 绘图：精确价格 & 久期近似
yields = np.linspace(y_min, y_max, 200)
prices_exact = [bond_price(y) for y in yields]
prices_tangent = P0 + P0 * (-mod_dur) * (yields - ytm_current)

plt.figure(figsize=(8, 5))
plt.plot(yields * 100, prices_exact, label='精确价格', linewidth=2)
plt.plot(yields * 100, prices_tangent, '--', label='久期近似（切线）', linewidth=2)
plt.axvline(ytm_current * 100, color='gray', linestyle=':', label=f'当前YTM ({ytm_current*100:.1f}%)')
plt.xlabel('到期收益率 (%)')
plt.ylabel('价格')
plt.title('债券价格-收益率曲线（面值100, 票息4.6%, 7年）')
plt.legend()
plt.grid(True)
figure_path = 'price_yield_curve.png'
plt.savefig(figure_path, dpi=150)
plt.show()

# 结果汇总
result = {
    'price_at_up100bp': P_new,
    'dur_approx_change_up100bp': dur_approx_relative_change,
    'figure_path': figure_path
}

print(result)
