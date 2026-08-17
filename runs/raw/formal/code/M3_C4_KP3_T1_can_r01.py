import numpy as np

# ==================== 债券参数设置 ====================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 (4.6%)
T = 7                       # 期限 (7年)
y = 0.053                   # 到期收益率 (5.3%)

# ==================== 步骤1：计算债券价格 ====================
# 构建现金流时间点与现金流向量
t = np.arange(1, T + 1)
cash_flows = np.full(T, face_value * coupon_rate)
cash_flows[-1] += face_value  # 最后一期还本付息

# 按年复利贴现
discount_factors = (1 + y) ** t
present_values = cash_flows / discount_factors
price = np.sum(present_values)

# ==================== 步骤2：计算麦考利久期与修正久期 ====================
# 麦考利久期 = Σ [ t * CF_t / (1+y)^t ] / P
macaulay_duration = np.sum(t * present_values) / price

# 修正久期 = 麦考利久期 / (1+y)
modified_duration = macaulay_duration / (1 + y)

# ==================== 步骤3：计算凸性 ====================
# 凸性 = Σ [ t(t+1) * CF_t / (1+y)^(t+2) ] / P
convexity_numerator = t * (t + 1) * cash_flows / ((1 + y) ** (t + 2))
convexity = np.sum(convexity_numerator) / price

# ==================== 步骤4：填充结果 ====================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 控制台输出，方便投屏展示计算结果
print("="*50)
print("《证券投资学》债券定价与久期、凸性计算结果")
print("="*50)
print(f"债券面值: {face_value}  |  票息率: {coupon_rate*100:.1f}%  |  期限: {T}年  |  YTM: {y*100:.1f}%")
print("-"*50)
print(f"价格 (Price)              : {result['price']:.4f}")
print(f"麦考利久期 (MacDur)       : {result['macaulay_duration_years']:.4f} 年")
print(f"修正久期 (ModDur)         : {result['modified_duration_years']:.4f} 年")
print(f"凸性 (Convexity)          : {result['convexity']:.4f} (年^2)")
print("="*50)
