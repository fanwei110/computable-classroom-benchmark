import numpy as np

# ---------- 债券参数 ----------
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率
years_to_maturity = 7       # 剩余年限
ytm = 0.053                 # 到期收益率

# ---------- 1. 价格计算 ----------
# 现金流时间：1,2,...,7
t = np.arange(1, years_to_maturity + 1)

# 票息现金流（每次支付）
coupon_payment = face_value * coupon_rate

# 所有现金流：前6年只付票息，最后一年票息+面值
cash_flows = np.full(years_to_maturity, coupon_payment)
cash_flows[-1] += face_value   # 加回面值

# 贴现因子
discount_factors = (1 + ytm) ** (-t)

# 价格 = 现金流贴现之和
price = np.sum(cash_flows * discount_factors)

# ---------- 2. 麦考利久期 ----------
# 麦考利久期 = Σ[ t * CF_t / (1+y)^t ] / P
macaulay_duration = np.sum(t * cash_flows * discount_factors) / price

# 修正久期 = 麦考利久期 / (1 + ytm)
modified_duration = macaulay_duration / (1 + ytm)

# ---------- 3. 凸性 ----------
# 凸性 = Σ[ t(t+1) * CF_t / (1+y)^(t+2) ] / P
convexity = np.sum(t * (t + 1) * cash_flows / ((1 + ytm) ** (t + 2))) / price

# ---------- 4. 结果字典 ----------
result = {
    'price': round(price, 6),
    'macaulay_duration_years': round(macaulay_duration, 6),
    'modified_duration_years': round(modified_duration, 6),
    'convexity': round(convexity, 6)
}

# 输出结果
print(result)
