import numpy as np

# 债券基本参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
years_to_maturity = 7       # 期限 7 年
ytm = 0.053                 # 到期收益率 5.3%

# 计算各期现金流
coupon_payment = face_value * coupon_rate
times = np.arange(1, years_to_maturity + 1)
cash_flows = np.full(years_to_maturity, coupon_payment)
cash_flows[-1] += face_value  # 最后一期加上本金

# 折现因子
discount_factors = (1 + ytm) ** times

# 各期现金流现值
pv_cash_flows = cash_flows / discount_factors

# 1. 计算债券价格
price = np.sum(pv_cash_flows)

# 2. 计算麦考利久期
# 公式: Macaulay Duration = Sum(t * PV(CF_t)) / Price
macaulay_duration = np.sum(times * pv_cash_flows) / price

# 3. 计算修正久期
# 公式: Modified Duration = Macaulay Duration / (1 + ytm)
modified_duration = macaulay_duration / (1 + ytm)

# 4. 计算凸性
# 公式: Convexity = (1/Price) * Sum( t(t+1) * CF_t / (1+ytm)^(t+2) )
# 等价于：Convexity = Sum( t(t+1) * PV(CF_t) ) / (Price * (1+ytm)^2)
convexity = np.sum(times * (times + 1) * cash_flows / ((1 + ytm) ** (times + 2))) / price

# 将结果存入字典，键名严格匹配要求
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 打印输出以供验证
for key, value in result.items():
    print(f"{key}: {value:.6f}")
