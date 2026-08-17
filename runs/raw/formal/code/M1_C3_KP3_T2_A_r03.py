import numpy as np
import matplotlib.pyplot as plt
import os

# 参数
face_value = 100
coupon_rate = 0.046
years = 7
initial_yield = 0.053
yield_change_bp = 100  # 100个基点 = 1%
yields = np.linspace(0.02, 0.09, 100)  # 2%到9%

# 计算精确价格
def bond_price(yield_rate, face_value, coupon_rate, years):
    coupon = face_value * coupon_rate
    price = sum([coupon / (1 + yield_rate) ** t for t in range(1, years + 1)]) + face_value / (1 + yield_rate) ** years
    return price

prices = [bond_price(y, face_value, coupon_rate, years) for y in yields]

# 计算久期和修正久期
def macaulay_duration(yield_rate, face_value, coupon_rate, years):
    coupon = face_value * coupon_rate
    duration = sum([t * coupon / (1 + yield_rate) ** t for t in range(1, years + 1)]) + years * face_value / (1 + yield_rate) ** years
    duration /= bond_price(yield_rate, face_value, coupon_rate, years)
    return duration

def modified_duration(yield_rate, face_value, coupon_rate, years):
    return macaulay_duration(yield_rate, face_value, coupon_rate, years) / (1 + yield_rate)

mod_dur = modified_duration(initial_yield, face_value, coupon_rate, years)

# 久期近似价格变化
approx_prices = [bond_price(initial_yield, face_value, coupon_rate, years) * (1 - mod_dur * (y - initial_yield)) for y in yields]

# 收益率上升100bp后的精确价格
new_yield = initial_yield + yield_change_bp / 10000
price_up100bp = bond_price(new_yield, face_value, coupon_rate, years)

# 久期近似相对价格变化
dur_approx_change = -mod_dur * (new_yield - initial_yield)

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yields, prices, label='精确价格', color='blue')
plt.plot(yields, approx_prices, label='久期近似', color='red', linestyle='--')
plt.scatter(initial_yield, bond_price(initial_yield, face_value, coupon_rate, years), color='green', zorder=5)
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
