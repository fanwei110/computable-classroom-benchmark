import numpy as np

# ========== 债券参数 ==========
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
coupon = face_value * coupon_rate   # 每年票息额
maturity = 7                # 剩余期限（年）
yield_rate = 0.053          # 到期收益率 5.3%

# 现金流向量：第1年到第7年
# 第1-6年：票息；第7年：票息 + 面值
cash_flows = np.full(maturity, coupon)
cash_flows[-1] += face_value   # 最后一年加上面值

# 时间向量 t = 1, 2, ..., 7
t = np.arange(1, maturity + 1)

# ---------- 1. 价格 ----------
# 贴现因子： 1/(1+y)^t
discount_factors = 1.0 / (1 + yield_rate) ** t
price = np.sum(cash_flows * discount_factors)

# ---------- 2. 麦考利久期 ----------
# 麦考利久期 = Σ [t * CF_t / (1+y)^t] / 价格
weighted_time = t * cash_flows * discount_factors
macaulay_duration = np.sum(weighted_time) / price   # 单位：年

# ---------- 3. 修正久期 ----------
modified_duration = macaulay_duration / (1 + yield_rate)

# ---------- 4. 凸性 ----------
# 凸性 = Σ [ t(t+1) * CF_t / (1+y)^(t+2) ] / 价格
# 因子 numerator: t(t+1) * CF_t / (1+y)^(t+2)
convexity_numerator = t * (t + 1) * cash_flows / (1 + yield_rate) ** (t + 2)
convexity = np.sum(convexity_numerator) / price

# ---------- 输出字典 ----------
result = {
    'price': round(price, 4),
    'macaulay_duration_years': round(macaulay_duration, 4),
    'modified_duration_years': round(modified_duration, 4),
    'convexity': round(convexity, 4)
}

# 打印详细结果（便于课堂展示）
print("=" * 50)
print("债券定价与风险分析结果")
print("=" * 50)
print(f"面值:                {face_value}")
print(f"票息率:              {coupon_rate*100:.2f}%")
print(f"期限:                {maturity} 年")
print(f"到期收益率:          {yield_rate*100:.2f}%")
print("-" * 50)
print(f"价格:                {result['price']:.4f}")
print(f"麦考利久期:          {result['macaulay_duration_years']:.4f} 年")
print(f"修正久期:            {result['modified_duration_years']:.4f} 年")
print(f"凸性:                {result['convexity']:.4f} 年²")
print("=" * 50)

# 验证结果：久期与凸性的经济含义展示
print("\n敏感性分析（收益率变动±1%）：")
delta_y = 0.01
# 实际价格变动
price_up = np.sum(cash_flows / (1 + yield_rate + delta_y) ** t)
price_down = np.sum(cash_flows / (1 + yield_rate - delta_y) ** t)

# 一阶近似（仅久期）
price_change_linear_up = -modified_duration * delta_y * price
price_change_linear_down = -modified_duration * (-delta_y) * price

# 二阶近似（久期+凸性）
price_change_convex_up = (-modified_duration * delta_y + 0.5 * convexity * delta_y**2) * price
price_change_convex_down = (-modified_duration * (-delta_y) + 0.5 * convexity * (-delta_y)**2) * price

print(f"收益率上升1% -> 实际价格: {price_up:.4f}, 线性近似: {price + price_change_linear_up:.4f}, 凸性近似: {price + price_change_convex_up:.4f}")
print(f"收益率下降1% -> 实际价格: {price_down:.4f}, 线性近似: {price + price_change_linear_down:.4f}, 凸性近似: {price + price_change_convex_down:.4f}")
