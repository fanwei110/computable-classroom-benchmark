import numpy as np

# 债券参数
face_value = 100          # 面值
coupon_rate = 0.046       # 票息率（年化）
years = 7                 # 剩余期限（年）
ytm = 0.053               # 到期收益率（报价收益率）

# 现金流时间（假设每年付息一次，整数年）
t = np.arange(1, years + 1)   # [1, 2, 3, ..., 7]

# 各期现金流（最后一期包含面值）
cash_flows = np.full(years, face_value * coupon_rate)  # 中间票息
cash_flows[-1] += face_value                           # 最后一期加上本金

# 贴现因子
discount_factors = (1 + ytm) ** t
present_values = cash_flows / discount_factors

# 1. 价格（现金流贴现之和）
price = np.sum(present_values)

# 2. 麦考利久期 = Σ [ t * PV(CF_t) ] / price
weighted_times = t * present_values
macaulay_duration_years = np.sum(weighted_times) / price

# 修正久期 = 麦考利久期 / (1 + ytm)
modified_duration_years = macaulay_duration_years / (1 + ytm)

# 3. 凸性 = Σ [ t*(t+1) * PV(CF_t) ] / (price * (1+ytm)^2 )
convexity_numerator = np.sum(t * (t + 1) * present_values)
convexity = convexity_numerator / (price * (1 + ytm)**2)

# 4. 输出结果字典
result = {
    'price': round(price, 6),
    'macaulay_duration_years': round(macaulay_duration_years, 6),
    'modified_duration_years': round(modified_duration_years, 6),
    'convexity': round(convexity, 6)
}

# 展示结果（便于投屏时直接看到）
print("债券计算结果（面值100, 票息4.6%, 7年, 收益率5.3%）")
print("------------------------------------------------")
print(f"价格 (Price)                         : {result['price']}")
print(f"麦考利久期 (Macaulay Duration)       : {result['macaulay_duration_years']} 年")
print(f"修正久期 (Modified Duration)         : {result['modified_duration_years']} 年")
print(f"凸性 (Convexity)                     : {result['convexity']}")
