import numpy as np

# ---------- 债券参数 ----------
face_value = 100.0
coupon_rate = 0.046
ytm = 0.053
n_periods = 7
coupon = face_value * coupon_rate

# ---------- 1. 计算价格 ----------
# 现金流：前6期利息，第7期利息+本金
cash_flows = np.full(n_periods, coupon)
cash_flows[-1] += face_value

# 折现因子
discount_factors = (1 + ytm) ** np.arange(1, n_periods + 1)
pv_cash_flows = cash_flows / discount_factors
price = np.sum(pv_cash_flows)

# ---------- 2. 计算麦考利久期和修正久期 ----------
# 麦考利久期 = Σ (t * PV(CF_t)) / price
times = np.arange(1, n_periods + 1)
weighted_times = times * pv_cash_flows
macaulay_duration = np.sum(weighted_times) / price

# 修正久期 = 麦考利久期 / (1 + YTM)
modified_duration = macaulay_duration / (1 + ytm)

# ---------- 3. 计算凸性 ----------
# 凸性 = [ Σ t*(t+1)*PV(CF_t) ] / [ price * (1+YTM)^2 ]
t_t_plus_1 = times * (times + 1)
weighted_convex = t_t_plus_1 * pv_cash_flows
convexity = np.sum(weighted_convex) / (price * (1 + ytm) ** 2)

# ---------- 4. 填充结果 ----------
result = {
    'price': round(price, 6),
    'macaulay_duration_years': round(macaulay_duration, 6),
    'modified_duration_years': round(modified_duration, 6),
    'convexity': round(convexity, 6)
}

# 打印输出（便于投屏查看）
for key, value in result.items():
    print(f"{key}: {value}")
