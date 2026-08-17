import numpy as np

# 债券参数设置
face_value = 100.0       # 面值
coupon_rate = 0.046      # 票息率 4.6%
maturity = 7            # 期限 7 年
y = 0.053               # 到期收益率 5.3%

# 计算每年现金流
times = np.arange(1, maturity + 1)
cash_flows = np.full(maturity, coupon_rate * face_value)
cash_flows[-1] += face_value  # 最后一期加入面值

# 1. 计算债券价格 (现金流贴现之和)
discount_factors = (1 + y) ** times
pv_cash_flows = cash_flows / discount_factors
price = np.sum(pv_cash_flows)

# 2. 计算麦考利久期与修正久期
# 麦考利久期 = Σ [t * CF_t / (1+y)^t] / P
macaulay_duration = np.sum(times * pv_cash_flows) / price

# 修正久期 = 麦考利久期 / (1+y)
modified_duration = macaulay_duration / (1 + y)

# 3. 计算凸性
# 凸性 = Σ [t(t+1)CF_t / (1+y)^(t+2)] / P
convexity_numerator = np.sum(times * (times + 1) * cash_flows / (1 + y) ** (times + 2))
convexity = convexity_numerator / price

# 4. 填充结果字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 控制台输出以便投屏展示
print("="*50)
print("债券定价与久期、凸性计算结果")
print("="*50)
for key, value in result.items():
    print(f"{key:<30}: {value:.6f}")
print("="*50)
