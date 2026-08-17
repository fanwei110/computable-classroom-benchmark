import numpy as np

# 债券参数
face_value = 100.0
coupon_rate = 0.046  # 4.6% 年票息
maturity_years = 7
yield_to_maturity = 0.053  # 5.3% 到期收益率
coupon_payment = face_value * coupon_rate  # 每年票息 = 4.6

# 现金流时间点：1 到 7 年
t = np.arange(1, maturity_years + 1, dtype=float)

# 各期现金流：前 6 年只有票息，第 7 年票息 + 面值
cash_flows = np.full(maturity_years, coupon_payment)
cash_flows[-1] += face_value  # 最后一年加上本金

# 折现因子
discount_factors = (1 + yield_to_maturity) ** t
present_values = cash_flows / discount_factors

# 1. 债券价格
price = np.sum(present_values)

# 2. 麦考利久期（年）
weights = present_values / price
macaulay_duration = np.sum(t * weights)

# 3. 修正久期（年）
modified_duration = macaulay_duration / (1 + yield_to_maturity)

# 4. 凸性
# 常用凸性公式：C = (1/P) * Σ [ CF_t * t * (t+1) / (1+y)^(t+2) ]
convexity = np.sum(cash_flows * t * (t + 1) / (1 + yield_to_maturity) ** (t + 2)) / price

# 按要求构造结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

if __name__ == '__main__':
    # 输出确定可复现的结果
    for key, value in result.items():
        print(f"{key}: {value:.6f}")
