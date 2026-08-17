import numpy as np

# ---------- 债券参数 ----------
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率（小数）
ytm = 0.053                 # 到期收益率（小数）
n_periods = 7               # 剩余年限

# ---------- 现金流向量 ----------
coupon = face_value * coupon_rate          # 每年票息 = 4.6
t = np.arange(1, n_periods + 1)            # 时间指标：1,2,...,7
cash_flows = np.full(n_periods, coupon)    # 前6年均为票息
cash_flows[-1] += face_value               # 最后一年加上本金

# ---------- 1. 价格 ----------
discount_factors = (1 + ytm) ** (-t)
present_values = cash_flows * discount_factors
price = np.sum(present_values)

# ---------- 2. 麦考利久期 & 修正久期 ----------
weights = present_values / price
macaulay_duration = np.sum(t * weights)                # 麦考利久期
modified_duration = macaulay_duration / (1 + ytm)      # 修正久期

# ---------- 3. 凸性 ----------
# 公式：凸性 = Σ[ t*(t+1) * CF_t / (1+y)^(t+2) ] / P
convexity_numerator = np.sum(
    t * (t + 1) * cash_flows / (1 + ytm) ** (t + 2)
)
convexity = convexity_numerator / price

# ---------- 汇总输出 ----------
result = {
    'price': round(price, 6),                    # 保留6位小数，清晰展示
    'macaulay_duration_years': round(macaulay_duration, 6),
    'modified_duration_years': round(modified_duration, 6),
    'convexity': round(convexity, 6)
}

# 打印结果，方便课堂投屏查看
print(result)
