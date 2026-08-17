import numpy as np
import matplotlib.pyplot as plt

# 债券参数
face_value = 100
coupon_rate = 0.046
coupon = face_value * coupon_rate
years = 7
ytm0 = 0.053  # 当前到期收益率

# 价格计算函数（年付息）
def bond_price(ytm):
    t = np.arange(1, years + 1)
    pv_coupons = np.sum(coupon / (1 + ytm) ** t)
    pv_face = face_value / (1 + ytm) ** years
    return pv_coupons + pv_face

# 麦考利久期
def macaulay_duration(ytm):
    t = np.arange(1, years + 1)
    pv_cf = coupon / (1 + ytm) ** t
    pv_face = face_value / (1 + ytm) ** years
    weighted_sum = np.sum(t * pv_cf) + years * pv_face
    price = np.sum(pv_cf) + pv_face
    return weighted_sum / price

# 当前价格与修正久期
P0 = bond_price(ytm0)
D_mac = macaulay_duration(ytm0)
D_mod = D_mac / (1 + ytm0)

# 收益率变动幅度（可调）
delta_y = 0.01  # +100bp

# 收益率+100bp后的精确价格
ytm_up = ytm0 + delta_y
P_up = bond_price(ytm_up)

# 久期法估计的相对变化
dur_approx_change = -D_mod * delta_y

# 绘制精确价格曲线与久期近似直线
yields = np.linspace(0.02, 0.09, 500)
exact_prices = bond_price(yields)
approx_prices = P0 * (1 - D_mod * (yields - ytm0))

plt.figure(figsize=(10, 6))
plt.plot(yields * 100, exact_prices, label='精确价格', linewidth=2)
plt.plot(yields * 100, approx_prices, '--', label=f'久期近似 (修正久期={D_mod:.4f})', linewidth=2)
plt.axvline(ytm0 * 100, color='gray', linestyle=':', alpha=0.7, label=f'当前YTM={ytm0*100:.2f}%')
plt.axvline(ytm_up * 100, color='red', linestyle=':', alpha=0.7, label=f'变动后YTM={ytm_up*100:.2f}%')
plt.xlabel('到期收益率 (%)')
plt.ylabel('债券价格')
plt.title('价格-收益率曲线与久期近似')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 保存图片
figure_path = 'price_duration_curve.png'
plt.savefig(figure_path, dpi=150)
plt.close()

# 按要求存储结果
result = {
    'price_at_up100bp': round(P_up, 6),
    'dur_approx_change_up100bp': round(dur_approx_change, 6),
    'figure_path': figure_path
}

print(result)
