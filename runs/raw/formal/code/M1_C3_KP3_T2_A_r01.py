import numpy as np
import matplotlib.pyplot as plt
import os

# 参数
face_value = 100
coupon_rate = 0.046
years = 7
initial_yield = 0.053
yield_shift = 0.01  # 100基点

# 收益率范围
yields = np.linspace(0.02, 0.09, 100)

# 精确价格计算
def bond_price(y):
    coupon = face_value * coupon_rate
    price = sum([coupon / (1 + y) ** t for t in range(1, years + 1)]) + face_value / (1 + y) ** years
    return price

prices_exact = [bond_price(y) for y in yields]

# 久期和修正久期计算
def macaulay_duration(y):
    coupon = face_value * coupon_rate
    duration = sum([t * coupon / (1 + y) ** t for t in range(1, years + 1)]) + years * face_value / (1 + y) ** years
    duration /= bond_price(y)
    return duration

def modified_duration(y):
    return macaulay_duration(y) / (1 + y)

# 久期近似价格变化
initial_price = bond_price(initial_yield)
initial_mod_duration = modified_duration(initial_yield)
prices_approx = [initial_price * (1 - initial_mod_duration * (y - initial_yield)) for y in yields]

# 收益率上升100基点后的精确价格
yield_up100bp = initial_yield + yield_shift
price_up100bp = bond_price(yield_up100bp)

# 久期近似的相对价格变化
dur_approx_change = -initial_mod_duration * yield_shift

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yields, prices_exact, label='精确价格', color='blue')
plt.plot(yields, prices_approx, label='久期近似', color='red', linestyle='--')
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
