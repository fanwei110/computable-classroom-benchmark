import numpy as np

# ==================== 假设处理 ====================
# 1. 付息频率：题目未指明，按国内《证券投资学》惯例，假设为每年付息一次（Annual Coupon）。
# 2. 计日惯例：假设为精确的整数年，不考虑实际天数的计日惯例调整。
# 3. 凸性定义：采用标准二阶泰勒展开中的凸性定义，即 Convexity = (1/P) * Σ [ t(t+1)CF / (1+y)^(t+2) ]

# ==================== 基本参数 ====================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
years_to_maturity = 7       # 期限 7年
ytm = 0.053                 # 到期收益率 5.3%

# ==================== 1. 计算债券价格 ====================
# 构建时间序列 t = [1, 2, ..., 7]
t = np.arange(1, years_to_maturity + 1, dtype=float)

# 构建现金流：第1至6年为票息，第7年为票息+面值
cash_flows = np.full(years_to_maturity, face_value * coupon_rate)
cash_flows[-1] += face_value

# 计算贴现因子
discount_factors = (1 + ytm) ** t

# 价格 = 现金流贴现求和
price = np.sum(cash_flows / discount_factors)

# ==================== 2. 计算麦考利久期与修正久期 ====================
# 现金流现值
pv_cash_flows = cash_flows / discount_factors

# 麦考利久期 = Σ(t * PV(CF)) / P
macaulay_duration = np.sum(t * pv_cash_flows) / price

# 修正久期 = 麦考利久期 / (1 + y)
modified_duration = macaulay_duration / (1 + ytm)

# ==================== 3. 计算凸性 ====================
# 凸性 = (1/P) * Σ [ t(t+1) * CF / (1+y)^(t+2) ]
convexity = np.sum(t * (t + 1) * cash_flows / (1 + ytm) ** (t + 2)) / price

# ==================== 4. 填充 result ====================
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration, 4),
    'modified_duration_years': round(modified_duration, 4),
    'convexity': round(convexity, 4)
}

# 打印结果供课堂投屏展示
print("="*50)
print("《证券投资学》课堂演示：债券定价与久期、凸性")
print("="*50)
print(f"基本参数: 面值={face_value}, 票息率={coupon_rate*100}%, 期限={years_to_maturity}年, YTM={ytm*100}%")
print(f"假设条件: 每年付息一次")
print("-"*50)
print(f"债券价格 (Price)               : {result['price']:.4f}")
print(f"麦考利久期 (Macaulay Duration)  : {result['macaulay_duration_years']:.4f} 年")
print(f"修正久期 (Modified Duration)    : {result['modified_duration_years']:.4f} 年")
print(f"凸性 (Convexity)               : {result['convexity']:.4f}")
print("="*50)
