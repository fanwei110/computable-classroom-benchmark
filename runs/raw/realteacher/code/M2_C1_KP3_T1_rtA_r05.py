import numpy as np

# 债券参数
face_value = 100.0
coupon_rate = 0.046
ytm = 0.053
maturity = 7

coupon = face_value * coupon_rate  # 4.6
periods = np.arange(1, maturity + 1)

# 各期现金流
cash_flows = np.full(maturity, coupon)
cash_flows[-1] += face_value  # 最后一年加上本金

# 折现因子
discount_factors = (1 + ytm) ** (-periods)

# 1. 价格
pv_cf = cash_flows * discount_factors
price = np.sum(pv_cf)

# 2. 麦考利久期
weighted_pv = pv_cf * periods
macaulay_duration = np.sum(weighted_pv) / price

# 3. 修正久期
modified_duration = macaulay_duration / (1 + ytm)

# 4. 凸性 (使用常规的离散凸性公式: sum[ t*(t+1)*CF_t / (1+y)^(t+2) ] / P )
# 或者等效: 1/(P*(1+y)^2) * sum( t*(t+1)*CF_t / (1+y)^t )
t_plus_one = periods * (periods + 1)
weighted_convexity = t_plus_one * cash_flows * discount_factors
sum_convexity = np.sum(weighted_convexity)
convexity = sum_convexity / (price * (1 + ytm)**2)

# 存入字典
result = {
    'price': round(price, 6),  # 保留合理小数
    'macaulay_duration_years': round(macaulay_duration, 6),
    'modified_duration_years': round(modified_duration, 6),
    'convexity': round(convexity, 6)
}

print(result)
