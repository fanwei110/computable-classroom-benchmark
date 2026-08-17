import numpy as np

# ====================
# 债券基本参数
# ====================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
years_to_maturity = 7       # 期限 7年
ytm = 0.053                # 到期收益率 5.3%

# 假设处理：题目未指明付息频率，按国内《证券投资学》常规惯例，默认按年付息
freq = 1 

# 根据付息频率调整计算参数
periods = int(years_to_maturity * freq)
periodic_ytm = ytm / freq
periodic_coupon = face_value * coupon_rate / freq

# ====================
# 1. 构建现金流并计算价格
# ====================
# 生成各期现金流：前 6 期只有票息，最后 1 期票息+本金
times = np.arange(1, periods + 1)
cash_flows = np.full(periods, periodic_coupon)
cash_flows[-1] += face_value

# 贴现因子与现值
discount_factors = (1 + periodic_ytm) ** times
pv_cash_flows = cash_flows / discount_factors
price = np.sum(pv_cash_flows)

# ====================
# 2. 计算麦考利久期与修正久期
# ====================
# 麦考利久期(按期) = Sum(t * PV(CF_t)) / Price
macaulay_duration_periods = np.sum(times * pv_cash_flows) / price

# 转换为以年为单位的麦考利久期
macaulay_duration_years = macaulay_duration_periods / freq

# 修正久期(按期) = 麦考利久期(按期) / (1 + 每期收益率)
modified_duration_periods = macaulay_duration_periods / (1 + periodic_ytm)

# 转换为以年为单位的修正久期
modified_duration_years = modified_duration_periods / freq

# ====================
# 3. 计算凸性
# ====================
# 凸性(按期)公式 = (1/P) * Sum[ CF_t * t * (t+1) / (1+y)^(t+2) ]
convexity_periods = np.sum(
    cash_flows * times * (times + 1) / ((1 + periodic_ytm) ** (times + 2))
) / price

# 转换为年化凸性 (年化凸性 = 按期凸性 / 频率^2)
convexity = convexity_periods / (freq ** 2)

# ====================
# 4. 填充 result 字典
# ====================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# ====================
# 控制台输出展示 (便于投屏查看)
# ====================
print("="*50)
print("《证券投资学》课堂实时计算结果")
print("="*50)
print(f"假设: 按年付息 (频率 = {freq})")
print(f"债券价格 (Price)           : {result['price']:.6f}")
print(f"麦考利久期 (Macaulay Dur.)  : {result['macaulay_duration_years']:.6f} 年")
print(f"修正久期 (Modified Dur.)   : {result['modified_duration_years']:.6f} 年")
print(f"凸性 (Convexity)           : {result['convexity']:.6f}")
print("="*50)
