import numpy as np
import matplotlib.pyplot as plt
import os

# 债券参数
face_value = 100
coupon_rate = 0.046
ytm = 0.053
years = 7
coupon = face_value * coupon_rate

# 计算债券价格
def bond_price(y, face_value, coupon, years):
    price = sum([coupon / (1 + y) ** t for t in range(1, years + 1)]) + face_value / (1 + y) ** years
    return price

# 计算久期
def macaulay_duration(y, face_value, coupon, years):
    discounted_cash_flows = [coupon / (1 + y) ** t for t in range(1, years + 1)] + [face_value / (1 + y) ** years]
    weights = [t * cf for t, cf in zip(range(1, years + 1), discounted_cash_flows[:-1])] + [years * discounted_cash_flows[-1]]
    duration = sum(weights) / sum(discounted_cash_flows)
    return duration

# 收益率范围
yields = np.linspace(0.02, 0.09, 100)
prices = [bond_price(y, face_value, coupon, years) for y in yields]

# 久期近似曲线（在ytm附近展开）
y0 = ytm
p0 = bond_price(y0, face_value, coupon, years)
duration = macaulay_duration(y0, face_value, coupon, years)
mod_duration = duration / (1 + y0)
approx_prices = [p0 * (1 - mod_duration * (y - y0)) for y in yields]

# 收益率+100bp后的精确价格
y_up100bp = ytm + 0.01
price_at_up100bp = bond_price(y_up100bp, face_value, coupon, years)

# 久期法估计的相对变化
dur_approx_change_up100bp = -mod_duration * 0.01

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(yields, prices, label='精确价格', color='blue')
plt.plot(yields, approx_prices, label='久期近似', color='red', linestyle='--')
plt.scatter([y0], [p0], color='green', zorder=5, label=f'YTM={y0*100:.1f}%')
plt.xlabel('收益率')
plt.ylabel('价格')
plt.title('债券价格与收益率曲线')
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
