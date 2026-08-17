import numpy as np

# ----- 债券参数（可根据需要修改） -----
face_value = 100.0         # 面值
coupon_rate = 0.046        # 票面利率（年化）
maturity = 7               # 期限（年）
ytm = 0.053                # 到期收益率（年化）
freq = 1                   # 付息频率（每年一次）

# ----- 生成现金流 -----
# 付息时间点（年末）：1, 2, ..., maturity
t = np.arange(1, maturity + 1, dtype=float)
# 每期票息（除最后一期加面值）
coupon = face_value * coupon_rate
cash_flows = np.full_like(t, coupon)
cash_flows[-1] += face_value  # 最后一期还本

# ----- 现金流贴现 -----
discount_factors = 1.0 / (1.0 + ytm) ** t
pv_cash_flows = cash_flows * discount_factors

# ----- 价格 -----
price = np.sum(pv_cash_flows)

# ----- 麦考利久期（Macaulay Duration） -----
weights = pv_cash_flows / price
macaulay_duration_years = np.sum(t * weights)

# ----- 修正久期（Modified Duration） -----
modified_duration_years = macaulay_duration_years / (1.0 + ytm)

# ----- 凸性（Convexity） -----
# 公式：Convexity = Σ[ t*(t+1) * PV(CF_t) ] / ( Price * (1+ytm)^2 )
convexity = np.sum(t * (t + 1) * pv_cash_flows) / (price * (1.0 + ytm) ** 2)

# ----- 按要求填充结果字典 -----
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 打印输出，便于课堂投屏查看
for key, value in result.items():
    print(f"{key}: {value:.6f}")
