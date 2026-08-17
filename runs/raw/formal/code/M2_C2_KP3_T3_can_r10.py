import numpy as np

# ==============================
# 债券参数设定（年付息假设）
# ==============================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票面利率 4.6%
yield_rate = 0.053          # 到期收益率 5.3%
maturity = 7                # 剩余期限 7 年
delta_y = 0.0080            # 收益率上升 80 个基点

# 构造现金流（每年付息一次，到期还本）
periods = np.arange(1, maturity + 1)
coupon = face_value * coupon_rate
cashflows = np.full(maturity, coupon)
cashflows[-1] += face_value  # 最后一期包含本金

# ==============================
# 1. 当前收益率下的定价与利率敏感性
# ==============================
discounts = (1 + yield_rate) ** (-periods)
pv_cashflows = cashflows * discounts
price = np.sum(pv_cashflows)

# 麦考利久期
weights = pv_cashflows / price
mac_duration = np.sum(periods * weights)

# 修正久期
mod_duration = mac_duration / (1 + yield_rate)

# 凸性（年付息公式：sum[ t(t+1)*PV ] / [ P * (1+y)^2 ]）
convexity = np.sum(periods * (periods + 1) * pv_cashflows) / (price * (1 + yield_rate)**2)

# ==============================
# 2. 估算收益率上升 80 bp 的价格影响（二阶泰勒近似）
# ==============================
# 价格变动比例
approx_delta_price_pct = -mod_duration * delta_y + 0.5 * convexity * (delta_y**2)
# 跌幅（百分比点数，正数表示价格下跌的百分比）
price_drop_pct = -approx_delta_price_pct * 100

# ==============================
# 3. 精确重定价（用于参考，不强制输出）
# ==============================
new_yield = yield_rate + delta_y
new_discounts = (1 + new_yield) ** (-periods)
new_price = np.sum(cashflows * new_discounts)
exact_delta_price_pct = (new_price - price) / price
exact_price_drop_pct = -exact_delta_price_pct * 100

# ==============================
# 输出结果
# ==============================
result = {
    'price_drop_pct': round(price_drop_pct, 4)   # 估算跌幅（%），正数
}

# 打印详细信息（方便课堂展示）
print("===== 债券基本信息 =====")
print(f"面值: {face_value}, 票息: {coupon_rate*100}%, 收益率: {yield_rate*100}%, 期限: {maturity}年")
print(f"当前全价: {price:.4f}")
print()
print("===== 利率敏感性 =====")
print(f"麦考利久期: {mac_duration:.4f} 年")
print(f"修正久期:   {mod_duration:.4f}")
print(f"凸性:       {convexity:.4f}")
print()
print("===== 收益率上升 80 bp 的影响 =====")
print(f"近似价格变动比率: {approx_delta_price_pct*100:.4f}%")
print(f"近似跌幅（正数）: {price_drop_pct:.4f}%")
print()
print("===== 精确重定价（参考） =====")
print(f"新收益率: {new_yield*100:.2f}%")
print(f"新全价:   {new_price:.4f}")
print(f"精确价格变动比率: {exact_delta_price_pct*100:.4f}%")
print(f"精确跌幅: {exact_price_drop_pct:.4f}%")
print()
print("===== 最终输出字典 =====")
print(result)
