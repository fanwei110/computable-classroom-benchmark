import numpy as np

# ==================== 参数设定 ====================
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率（年）
yield_rate = 0.053          # 当前收益率（年）
maturity = 7                # 期限（年）
shift = 0.0080              # 收益率上升 80 个基点

# 假设每年付息一次（标准假设，未指定时默认）
# =================================================

# ---------- 1. 计算当前价格（全价） ----------
# 现金流时间：1, 2, ..., maturity 年
cash_flow_times = np.arange(1, maturity + 1)
coupon_payment = face_value * coupon_rate
cash_flows = np.full(maturity, coupon_payment)
cash_flows[-1] += face_value  # 最后一年包含本金

# 贴现因子
discount_factors = (1 + yield_rate) ** (-cash_flow_times)
price = np.sum(cash_flows * discount_factors)

# ---------- 2. 计算麦考利久期与修正久期 ----------
# 现金流现值
pv_cash_flows = cash_flows * discount_factors
# 麦考利久期 = Σ(t * PV) / price
macaulay_duration = np.sum(cash_flow_times * pv_cash_flows) / price
# 修正久期 = 麦考利久期 / (1 + y)
modified_duration = macaulay_duration / (1 + yield_rate)

# ---------- 3. 计算凸性 ----------
# 凸性 = (1/(P*(1+y)^2)) * Σ [t*(t+1)*CF_t/(1+y)^t]
# 另一定义直接用： convexity = Σ [t*(t+1)*PV_t] / (P * (1+y)^2)
convexity = (np.sum(cash_flow_times * (cash_flow_times + 1) * pv_cash_flows)
             / (price * (1 + yield_rate)**2))

# ---------- 4. 估算价格变动百分比 ----------
# 利用修正久期与凸性近似：
# ΔP/P ≈ -MD * Δy + 0.5 * convexity * (Δy)^2
delta_y = shift
price_drop_pct_approx = -modified_duration * delta_y + 0.5 * convexity * (delta_y**2)
# price_drop_pct 定义为跌幅，正数表示价格下跌百分比
price_drop_pct = -price_drop_pct_approx * 100.0   # 转换为百分比点

# ---------- 5. 精确验证（可选，不硬性要求） ----------
new_yield = yield_rate + delta_y
new_discount_factors = (1 + new_yield) ** (-cash_flow_times)
new_price = np.sum(cash_flows * new_discount_factors)
actual_price_drop_pct = (price - new_price) / price * 100.0

# ==================== 输出结果 ====================
result = {
    'price_drop_pct': round(price_drop_pct, 4)
}

# （课堂展示可选打印）
if __name__ == '__main__':
    print(f"当前价格: {price:.4f}")
    print(f"修正久期: {modified_duration:.4f}")
    print(f"凸性: {convexity:.4f}")
    print(f"估算价格跌幅（80bp）: {price_drop_pct:.4f}%")
    print(f"实际精确跌幅: {actual_price_drop_pct:.4f}%")
    print("结果字典:", result)
