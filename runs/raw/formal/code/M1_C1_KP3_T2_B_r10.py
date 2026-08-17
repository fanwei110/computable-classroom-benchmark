import numpy as np
import matplotlib.pyplot as plt
import os

# 参数
face_value = 100
coupon_rate = 0.046
ytm = 0.053
n_years = 7
y_range = np.linspace(0.02, 0.09, 100)  # 2%到9%

# 计算精确价格
def bond_price(y, face_value, coupon_rate, n_years):
    coupon = face_value * coupon_rate
    price = sum([coupon / (1 + y)**t for t in range(1, n_years + 1)]) + face_value / (1 + y)**n_years
    return price

# 计算久期
def bond_duration(y, face_value, coupon_rate, n_years):
    coupon = face_value * coupon_rate
    mac_dur = sum([t * coupon / (1 + y)**t for t in range(1, n_years + 1)]) + n_years * face_value / (1 + y)**n_years
    mac_dur /= bond_price(y, face_value, coupon_rate, n_years)
    mod_dur = mac_dur / (1 + y)
    return mac_dur, mod_dur

# 基准价格和久期
base_price = bond_price(ytm, face_value, coupon_rate, n_years)
mac_dur, mod_dur = bond_duration(ytm, face_value, coupon_rate, n_years)

# 精确价格和久期近似价格
exact_prices = [bond_price(y, face_value, coupon_rate, n_years) for y in y_range]
approx_prices = [base_price * (1 - mod_dur * (y - ytm)) for y in y_range]

# 收益率+100bp后的结果
ytm_up100bp = ytm + 0.01
price_at_up100bp = bond_price(ytm_up100bp, face_value, coupon_rate, n_years)
dur_approx_change_up100bp = -mod_dur * 0.01 * 100  # 百分比变化

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(y_range * 100, exact_prices, label='精确价格', color='blue')
plt.plot(y_range * 100, approx_prices, label='久期近似', color='red', linestyle='--')
plt.xlabel('收益率 (%)')
plt.ylabel('价格')
plt.title('债券价格收益率曲线')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path)
plt.close()

# 结果字典
result = {
    'price_at_up100bp': price_at_up100bp,
    'dur_approx_change_up100bp': dur_approx_change_up100bp,
    'figure_path': os.path.abspath(figure_path)
}

print(result)
