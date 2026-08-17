import numpy as np
from scipy import optimize
import pandas as pd
import matplotlib.pyplot as plt

# 债券参数
face_value = 100  # 面值
coupon_rate = 0.046  # 票息率
years_to_maturity = 7  # 期限
ytm = 0.053  # 到期收益率
coupon_payment = face_value * coupon_rate  # 每年利息支付

# 定义时间点（年）
time_points = np.arange(1, years_to_maturity + 1)

# 计算现金流
cash_flows = np.full(years_to_maturity, coupon_payment)
cash_flows[-1] += face_value  # 最后一年加上本金

# 计算价格（现值之和）
discount_factors = np.exp(-ytm * time_points)  # 连续复利折现
# 或者使用离散复利（更标准）
discount_factors_discrete = (1 + ytm) ** (-time_points)
price = np.sum(cash_flows * discount_factors_discrete)

# 计算麦考利久期
# Macaulay Duration = sum(t * PV(CF_t)) / Price
present_values = cash_flows * discount_factors_discrete
weighted_time = np.sum(time_points * present_values)
macaulay_duration = weighted_time / price

# 计算修正久期
# Modified Duration = Macaulay Duration / (1 + ytm)
modified_duration = macaulay_duration / (1 + ytm)

# 计算凸性
# Convexity = sum(t * (t+1) * PV(CF_t)) / (Price * (1 + ytm)^2)
weighted_time_squared = np.sum(time_points * (time_points + 1) * present_values)
convexity = weighted_time_squared / (price * (1 + ytm)**2)

# 创建结果字典
result = {
    'price': float(price),
    'macaulay_duration_years': float(macaulay_duration),
    'modified_duration_years': float(modified_duration),
    'convexity': float(convexity)
}

# 打印结果
print("债券计算结果:")
print(f"价格 (Price): {result['price']:.4f}")
print(f"麦考利久期 (Macaulay Duration): {result['macaulay_duration_years']:.4f} 年")
print(f"修正久期 (Modified Duration): {result['modified_duration_years']:.4f} 年")
print(f"凸性 (Convexity): {result['convexity']:.4f}")

# 验证：使用收益率变化验证久期和凸性
print("\n验证（收益率变化±1%）:")
ytm_change = 0.01
# 直接计算新价格
new_ytm_up = ytm + ytm_change
new_discount_factors_up = (1 + new_ytm_up) ** (-time_points)
new_price_up = np.sum(cash_flows * new_discount_factors_up)

new_ytm_down = ytm - ytm_change
new_discount_factors_down = (1 + new_ytm_down) ** (-time_points)
new_price_down = np.sum(cash_flows * new_discount_factors_down)

# 使用久期和凸性近似
duration_approx_up = price * (1 - modified_duration * ytm_change + 0.5 * convexity * (ytm_change**2))
duration_approx_down = price * (1 + modified_duration * ytm_change + 0.5 * convexity * (ytm_change**2))

print(f"收益率+1%: 实际价格 {new_price_up:.4f}, 近似价格 {duration_approx_up:.4f}, 差异 {abs(new_price_up - duration_approx_up):.4f}")
print(f"收益率-1%: 实际价格 {new_price_down:.4f}, 近似价格 {duration_approx_down:.4f}, 差异 {abs(new_price_down - duration_approx_down):.4f}")

# 可选：可视化现金流
plt.figure(figsize=(10, 6))
plt.bar(time_points, cash_flows, alpha=0.7, color='blue', label='现金流')
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.xlabel('时间（年）')
plt.ylabel('现金流')
plt.title('债券现金流分布')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# 可选：展示半结构化表格
df = pd.DataFrame({
    '年份': time_points,
    '现金流': cash_flows,
    '折现因子': discount_factors_discrete,
    '现值': present_values,
    '权重': present_values / price
})
print("\n现金流分析表:")
print(df.to_string(index=False))
