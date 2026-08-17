import numpy as np

# ==================== 债券参数设置 ====================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票面利率 4.6%
years_to_maturity = 7       # 期限 7年
ytm = 0.053                 # 到期收益率 5.3%

# 假设处理：题目未指明付息频率，默认采用【年付息频率】(Annual Coupon Payments)
# 每期票息
coupon = face_value * coupon_rate

# ==================== 1. 计算债券价格 ====================
# 生成现金流时间序列 t = [1, 2, ..., 7]
t = np.arange(1, years_to_maturity + 1)

# 生成现金流：前6期仅票息，最后1期票息+面值
cash_flows = np.full(years_to_maturity, coupon)
cash_flows[-1] += face_value

# 贴现因子
discount_factors = (1 + ytm) ** t

# 现金流现值
pv_cash_flows = cash_flows / discount_factors

# 债券价格（现金流贴现之和）
price = np.sum(pv_cash_flows)

# ==================== 2. 计算麦考利久期与修正久期 ====================
# 麦考利久期 = (t * CF_t / (1+y)^t) 之和 / 价格
macaulay_duration = np.sum(t * pv_cash_flows) / price

# 修正久期 = 麦考利久期 / (1 + y)  (年付息频率下分母为 1+y)
modified_duration = macaulay_duration / (1 + ytm)

# ==================== 3. 计算凸性 ====================
# 凸性公式(年化)：Convexity = [ t*(t+1)*CF_t / (1+y)^(t+2) ] 之和 / P
# 等价于：Convexity = [ t*(t+1)*CF_t / (1+y)^t ] 之和 / [ P * (1+y)^2 ]
convexity = np.sum(t * (t + 1) * pv_cash_flows) / (price * (1 + ytm) ** 2)

# ==================== 4. 填充 result ====================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 课堂投屏展示结果（保留4位小数以观清晰）
print(f"债券价格: {result['price']:.4f}")
print(f"麦考利久期: {result['macaulay_duration_years']:.4f} 年")
print(f"修正久期: {result['modified_duration_years']:.4f} 年")
print(f"凸性: {result['convexity']:.4f}")
