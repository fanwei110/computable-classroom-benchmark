import numpy as np

# 债券参数
face_value = 100                # 面值
coupon_rate = 0.046             # 票息率 4.6%
years_to_maturity = 7           # 期限 7 年
ytm = 0.053                     # 到期收益率 5.3%

# 计算每年的现金流
# 每年票息 = 面值 * 票息率
coupon_payment = face_value * coupon_rate

# 生成时间序列 t = [1, 2, ..., 7]
t = np.arange(1, years_to_maturity + 1)

# 生成现金流序列：前 6 年为票息，第 7 年为票息 + 面值
cash_flows = np.full(years_to_maturity, coupon_payment)
cash_flows[-1] += face_value

# 折现因子
discount_factors = (1 + ytm) ** -t

# 现金流现值
pv_cash_flows = cash_flows * discount_factors

# 1. 计算价格 (Price)
price = np.sum(pv_cash_flows)

# 2. 计算麦考利久期 (Macaulay Duration)
# MacDur = Sum(t * PV_CF) / Price
macaulay_duration_years = np.sum(t * pv_cash_flows) / price

# 3. 计算修正久期 (Modified Duration)
# ModDur = MacDur / (1 + ytm)
modified_duration_years = macaulay_duration_years / (1 + ytm)

# 4. 计算凸性 (Convexity)
# Convexity = Sum(CF_t * t * (t+1) / (1+ytm)^(t+2)) / Price
convexity = np.sum(cash_flows * t * (t + 1) * (1 + ytm) ** -(t + 2)) / price

# 按照输出契约将结果存入字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 打印结果以供验证
for key, value in result.items():
    print(f"{key}: {value:.6f}")
