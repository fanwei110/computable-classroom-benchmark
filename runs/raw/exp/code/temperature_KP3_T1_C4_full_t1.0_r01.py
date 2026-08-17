import numpy as np

# --- 债券参数 ---
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
maturity_years = 7          # 期限7年
yield_to_maturity = 0.053   # 到期收益率 5.3%

# 每年现金流
coupon = face_value * coupon_rate  # 每年票息 = 4.6

# 现金流发生的时间点(第1年末到第7年末)
t = np.arange(1, maturity_years + 1)   # [1,2,3,4,5,6,7]

# 各期现金流：前6年只有票息，第7年有票息+面值
cash_flows = np.full(maturity_years, coupon)   # 所有年份都先填票息
cash_flows[-1] += face_value                    # 最后一年加上面值

# --- 1. 债券价格 (按年复利贴现) ---
discount_factors = (1 + yield_to_maturity) ** (-t)
price = np.sum(cash_flows * discount_factors)

# --- 2. 麦考利久期 (年) ---
macaulay_duration = np.sum(t * cash_flows * discount_factors) / price

# 修正久期
modified_duration = macaulay_duration / (1 + yield_to_maturity)

# --- 3. 凸性 (年平方) ---
# 凸性公式: sum[t(t+1)*CF/(1+y)^(t+2)] / Price
convexity_factor = t * (t + 1) * cash_flows / ((1 + yield_to_maturity) ** (t + 2))
convexity = np.sum(convexity_factor) / price

# --- 4. 结果字典 ---
result = {
    'price': round(price, 6),                        # 价格保留6位小数
    'macaulay_duration_years': round(macaulay_duration, 6),
    'modified_duration_years': round(modified_duration, 6),
    'convexity': round(convexity, 6)                 # 凸性单位为年平方
}

# 打印结果 (教师可展示)
print("计算结果:")
for key, val in result.items():
    print(f"{key}: {val}")
