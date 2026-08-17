# 债券参数
face_value = 100
coupon_rate = 0.046  # 年票息率
yield_to_maturity = 0.053  # 年到期收益率
years = 7  # 剩余年限

# 现金流：每年付息一次，最后一年加上本金
cash_flows = [coupon_rate * face_value] * (years - 1) + [coupon_rate * face_value + face_value]
times = list(range(1, years + 1))

# 价格计算：按年复利折现
pv_cfs = [cf / (1 + yield_to_maturity) ** t for cf, t in zip(cash_flows, times)]
price = sum(pv_cfs)

# 麦考利久期
weighted_times = [t * pv for t, pv in zip(times, pv_cfs)]
macaulay_duration = sum(weighted_times) / price

# 修正久期（年复利 => 修正久期 = 麦考利久期 / (1 + y)）
modified_duration = macaulay_duration / (1 + yield_to_maturity)

# 凸性 = Σ[t(t+1)*PV(CF)] / [Price * (1+y)^2]
convexity_numerator = sum(t * (t + 1) * pv for t, pv in zip(times, pv_cfs))
convexity = convexity_numerator / (price * (1 + yield_to_maturity) ** 2)

# 输出字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

result
