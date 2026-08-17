import numpy as np

# 债券参数
face_value = 100.0
coupon_rate = 0.046
yield_rate = 0.053
maturity = 7
delta_y = 0.0080  # 80个基点

# 现金流时间点 (年付息一次)
t = np.arange(1, maturity + 1)

# 现金流
coupon = face_value * coupon_rate
cash_flows = np.full(maturity, coupon)
cash_flows[-1] += face_value  # 最后一期加上本金

# 贴现因子
discount_factors = (1 + yield_rate) ** t
present_values = cash_flows / discount_factors

# 当前价格
price = np.sum(present_values)

# 麦考利久期 (Macaulay Duration)
weighted_t = t * present_values
macaulay_duration = np.sum(weighted_t) / price

# 修正久期 (Modified Duration)
modified_duration = macaulay_duration / (1 + yield_rate)

# 凸性 (Convexity) - 公式: Σ [t(t+1) * CF / (1+y)^{t+2}] / P
convexity = np.sum(t * (t + 1) * cash_flows / (1 + yield_rate) ** (t + 2)) / price

# 用久期和凸性近似价格变化百分比 (收益率上升80个基点)
# ΔP/P ≈ -MD * Δy + 0.5 * C * (Δy)^2
approx_price_change = -modified_duration * delta_y + 0.5 * convexity * (delta_y ** 2)
# 跌幅 (正数表示价格下跌)
approx_price_drop_pct = -approx_price_change * 100

# 精确价格计算 (用于验证)
new_yield = yield_rate + delta_y
new_discount_factors = (1 + new_yield) ** t
new_price = np.sum(cash_flows / new_discount_factors)
exact_price_drop_pct = (price - new_price) / price * 100

# 结果存入字典
result = {
    'price_drop_pct': round(approx_price_drop_pct, 6)
}

# 打印详细结果供课堂展示
print(f"当前收益率: {yield_rate*100:.2f}%")
print(f"债券价格: {price:.4f}")
print(f"麦考利久期: {macaulay_duration:.4f} 年")
print(f"修正久期: {modified_duration:.4f}")
print(f"凸性: {convexity:.4f}")
print(f"收益率上升 {delta_y*100:.0f} 个基点")
print(f"近似价格跌幅: {approx_price_drop_pct:.4f}%")
print(f"精确价格跌幅: {exact_price_drop_pct:.4f}%")
print(f"\nresult = {result}")
