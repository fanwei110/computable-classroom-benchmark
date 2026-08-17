import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import newton

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
maturity_years = 7          # 期限 7年
yield_to_maturity = 0.053   # 到期收益率 5.3%

# 生成现金流时间点（每年付息，第7年还本+付息）
t = np.arange(1, maturity_years + 1)                     # 1,2,...,7
coupon_payments = coupon_rate * face_value               # 每期票息
# 现金流向量：前6年为票息，最后一年为票息+面值
cf = np.full(maturity_years, coupon_payments)
cf[-1] += face_value

# 1. 计算价格：现金流贴现之和（年复利贴现）
discount_factors = (1 + yield_to_maturity) ** (-t)
price = np.dot(cf, discount_factors)

# 2. 计算麦考利久期 (MacDur = Σ t * CF_t / (1+y)^t / Price)
macaulay_duration = np.dot(t, cf * discount_factors) / price

# 修正久期 = 麦考利久期 / (1 + y)
modified_duration = macaulay_duration / (1 + yield_to_maturity)

# 3. 计算凸性 (Convexity = Σ t(t+1) * CF_t / (1+y)^(t+2) / Price)
# 分子：t*(t+1) * CF_t / (1+y)^(t+2)
convexity_numerator = np.sum(t * (t + 1) * cf / (1 + yield_to_maturity) ** (t + 2))
convexity = convexity_numerator / price

# 4. 结果字典
result = {
    'price': round(price, 6),
    'macaulay_duration_years': round(macaulay_duration, 6),
    'modified_duration_years': round(modified_duration, 6),
    'convexity': round(convexity, 6)
}

# 输出结果
print("计算结果如下：")
for key, value in result.items():
    print(f"{key}: {value}")

# 额外画图展示价格-收益率关系，显示在屏幕上（可选，教师可展示）
def bond_price(y):
    """给定收益率y（小数），返回债券价格"""
    t_ = np.arange(1, maturity_years + 1)
    cf_ = np.full(maturity_years, coupon_rate * face_value)
    cf_[-1] += face_value
    return np.dot(cf_, (1 + y) ** (-t_))

yields = np.linspace(0.02, 0.10, 200)
prices = [bond_price(y) for y in yields]

# 画图（非必需但有利于课堂展示）
plt.figure(figsize=(8, 5))
plt.plot(yields, prices, label='Bond Price', color='steelblue')
plt.axvline(x=yield_to_maturity, color='red', linestyle='--', label='YTM = 5.3%')
plt.axhline(y=price, color='grey', linestyle=':', alpha=0.7)
plt.xlabel('Yield to Maturity')
plt.ylabel('Bond Price')
plt.title('Bond Price vs YTM (7-year, 4.6% coupon)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# 确保 result 字典存在于当前命名空间，且包含所需键
assert set(result.keys()) == {'price', 'macaulay_duration_years', 'modified_duration_years', 'convexity'}
