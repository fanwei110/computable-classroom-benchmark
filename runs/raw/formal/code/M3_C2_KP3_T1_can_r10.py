import numpy as np

# ==================== 债券参数设定 ====================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 (4.6%)
n = 7                       # 期限 (7年)
ytm = 0.053                 # 到期收益率 (5.3%)

# 假设处理：题目未指明付息频率，按国内《证券投资学》常规，默认为按年付息
# "到期一次还本"即本金在第7年末随最后一期票息一起偿还（子弹型债券）
coupon_payment = face_value * coupon_rate  # 每年票息现金流

# ==================== 1. 计算价格 ====================
# 生成各期时间点与现金流
times = np.arange(1, n + 1)
cash_flows = np.full(n, coupon_payment)
cash_flows[-1] += face_value  # 最后一期加入面值

# 贴现因子并求和得价格
discount_factors = (1 + ytm) ** times
pv_cash_flows = cash_flows / discount_factors
price = np.sum(pv_cash_flows)

# ==================== 2. 计算麦考利久期与修正久期 ====================
# 麦考利久期 = (1/P) * sum(t * PV(CF_t))
macaulay_duration_years = np.sum(times * pv_cash_flows) / price

# 修正久期 = 麦考利久期 / (1 + y)
modified_duration_years = macaulay_duration_years / (1 + ytm)

# ==================== 3. 计算凸性 ====================
# 凸性的严谨数学推导来自价格对y的二阶导数：
# P'' = sum( CF_t * t * (t+1) / (1+y)^(t+2) )
# 凸性 C = P'' / P
convexity_numerator = np.sum(cash_flows * times * (times + 1) / (1 + ytm) ** (times + 2))
convexity = convexity_numerator / price

# ==================== 4. 填充 result ====================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# ==================== 结果输出展示 ====================
print("="*50)
print("债券定价与久期、凸性计算结果")
print("="*50)
print(f"假设: 按年付息，到期一次还本 (YTM={ytm*100:.1f}%)")
print("-"*50)
print(f"价格 (Price)              : {result['price']:.4f}")
print(f"麦考利久期 (Macaulay Dur) : {result['macaulay_duration_years']:.4f} 年")
print(f"修正久期 (Modified Dur)   : {result['modified_duration_years']:.4f} 年")
print(f"凸性 (Convexity)          : {result['convexity']:.4f}")
print("="*50)
