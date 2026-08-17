import numpy as np
import matplotlib.pyplot as plt
import os

# 参数
face_value = 100
coupon_rate = 0.046
years = 7
initial_yield = 0.053
yield_range = np.linspace(0.02, 0.09, 100)  # 2%到9%

# 计算精确价格
def bond_price(yield_rate, face_value, coupon_rate, years):
    coupon = face_value * coupon_rate
    price = sum([coupon / (1 + yield_rate) ** t for t in range(1, years + 1)]) + face_value / (1 + yield_rate) ** years
    return price

# 计算久期
def macaulay_duration(yield_rate, face_value, coupon_rate, years):
    coupon = face_value * coupon_rate
    weighted_cashflows = sum([t * coupon / (1 + yield_rate) ** t for t in range(1, years + 1)]) + years * face_value / (1 + yield_rate) ** years
    price = bond_price(yield_rate, face_value, coupon_rate, years)
    return weighted_cashflows / price

# 计算修正久期
def modified_duration(yield_rate, face_value, coupon_rate, years):
    mac_dur = macaulay_duration(yield_rate, face_value, coupon_rate, years)
    return mac_dur / (1 + yield_rate)

# 计算精确价格曲线
prices = [bond_price(y, face_value, coupon_rate, years) for y in yield_range]

# 计算久期近似曲线（在初始收益率附近线性近似）
initial_price = bond_price(initial_yield, face_value, coupon_rate, years)
mod_dur = modified_duration(initial_yield, face_value, coupon_rate, years)
approx_prices = [initial_price * (1 - mod_dur * (y - initial_yield)) for y in yield_range]

# 收益率上升100bp后的精确价格
yield_up100bp = initial_yield + 0.01
price_up100bp = bond_price(yield_up100bp, face_value, coupon_rate, years)

# 久期近似的相对价格变化
dur_approx_change = -mod_dur * 0.01

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yield_range, prices, label='精确价格', color='blue')
plt.plot(yield_range, approx_prices, label='久期近似', color='red', linestyle='--')
plt.axvline(initial_yield, color='gray', linestyle=':', label='初始收益率 (5.3%)')
plt.xlabel('收益率')
plt.ylabel('债券价格')
plt.title('债券价格随收益率变化')
plt.legend()
plt.grid(True)

# 保存图片
figure_path = 'bond_price_vs_yield.png'
plt.savefig(figure_path)
plt.close()

# 结果字典
result = {
    'price_at_up100bp': price_up100bp,
    'dur_approx_change_up100bp': dur_approx_change,
    'figure_path': os.path.abspath(figure_path)
}

result
