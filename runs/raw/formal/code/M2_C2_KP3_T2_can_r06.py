import numpy as np
import matplotlib.pyplot as plt

# 债券参数
face_value = 100
coupon_rate = 0.046
years = 7
current_yield = 0.053

# 票息支付频率（默认假设每年付息一次）
frequency = 1

def bond_price(ytm, face_value, coupon_rate, years, frequency=1):
    """计算债券价格"""
    coupon = coupon_rate * face_value / frequency
    periods = years * frequency
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value
    
    discount_factors = [(1 + ytm / frequency) ** (-t) for t in range(1, periods + 1)]
    price = np.sum(cash_flows * discount_factors)
    return price

def macaulay_duration(ytm, face_value, coupon_rate, years, frequency=1):
    """计算麦考利久期"""
    coupon = coupon_rate * face_value / frequency
    periods = years * frequency
    cash_flows = np.full(periods, coupon)
    cash_flows[-1] += face_value
    
    discount_factors = [(1 + ytm / frequency) ** (-t) for t in range(1, periods + 1)]
    pv_cf = cash_flows * discount_factors
    price = np.sum(pv_cf)
    
    times = np.arange(1, periods + 1) / frequency
    mac_duration = np.sum(times * pv_cf) / price
    return mac_duration

def modified_duration(ytm, face_value, coupon_rate, years, frequency=1):
    """计算修正久期"""
    mac_dur = macaulay_duration(ytm, face_value, coupon_rate, years, frequency)
    mod_dur = mac_dur / (1 + ytm / frequency)
    return mod_dur

# 1. 计算定价-收益率曲线的收益率网格
yields_grid = np.linspace(0.02, 0.09, 100)

# 计算精确价格
exact_prices = [bond_price(y, face_value, coupon_rate, years, frequency) for y in yields_grid]

# 计算当前收益率下的价格和久期
current_price = bond_price(current_yield, face_value, coupon_rate, years, frequency)
mod_dur_current = modified_duration(current_yield, face_value, coupon_rate, years, frequency)

# 计算久期近似的价格（使用泰勒展开的一次项）
dur_prices = [current_price - mod_dur_current * current_price * (y - current_yield) 
              for y in yields_grid]

# 2. 收益率上升100个基点后的精确价格
target_yield = current_yield + 0.01  # 上升100bp
price_at_up100bp = bond_price(target_yield, face_value, coupon_rate, years, frequency)

# 久期法估计的相对价格变化
dur_approx_change_up100bp = -mod_dur_current * 0.01 * 100  # 百分比变化

# 3. 绘图
plt.figure(figsize=(12, 8))
plt.plot(yields_grid * 100, exact_prices, 'b-', label='Exact Price', linewidth=2)
plt.plot(yields_grid * 100, dur_prices, 'r--', label='Duration-Based Approximation', linewidth=2)
plt.axvline(x=current_yield * 100, color='g', linestyle=':', label=f'Current Yield ({current_yield*100:.1f}%)')
plt.axhline(y=current_price, color='gray', linestyle=':', alpha=0.5)

plt.xlabel('Yield to Maturity (%)', fontsize=12)
plt.ylabel('Bond Price', fontsize=12)
plt.title('Bond Price vs Yield Curve\n(Face Value: 100, Coupon: 4.6%, Years: 7)', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)

# 设置坐标轴范围
plt.xlim(2, 9)
plt.ylim(min(exact_prices) - 1, max(exact_prices) + 1)

# 保存图形
figure_path = 'bond_price_yield_curve.png'
plt.savefig(figure_path, dpi=150, bbox_inches='tight')
plt.close()

# 4. 填充结果字典
result = {
    'price_at_up100bp': round(float(price_at_up100bp), 6),
    'dur_approx_change_up100bp': round(float(dur_approx_change_up100bp), 6),
    'figure_path': figure_path
}

print("计算结果:")
print(f"收益率上升100bp后的精确价格: {result['price_at_up100bp']:.6f}")
print(f"久期法估计的相对价格变化: {result['dur_approx_change_up100bp']:.6f}%")
print(f"图形已保存至: {result['figure_path']}")
