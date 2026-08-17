import numpy as np

# 债券参数
face_value = 100.0       # 面值
coupon_rate = 0.046      # 票息率
years = 7                # 期限（年）
ytm = 0.053              # 到期收益率

# 现金流时间点：1, 2, ..., years
t = np.arange(1, years + 1)

# 现金流：每年票息 + 最后一年本金
coupon = face_value * coupon_rate
cash_flows = np.full(years, coupon)
cash_flows[-1] += face_value  # 最后一次还本付息

# 贴现因子
discount_factors = (1 + ytm) ** t

# 各现金流现值
pv_cf = cash_flows / discount_factors

# 1. 价格
price = np.sum(pv_cf)

# 2. 麦考利久期 Macaulay duration
macaulay_duration = np.sum(t * pv_cf) / price

# 修正久期 Modified duration
modified_duration = macaulay_duration / (1 + ytm)

# 3. 凸性 Convexity = (1/P) * d^2P/dy^2
# d^2P/dy^2 = sum( t*(t+1)*CF_t / (1+y)^{t+2} )
d2P_dy2 = np.sum(t * (t + 1) * cash_flows / (1 + ytm) ** (t + 2))
convexity = d2P_dy2 / price

# 输出存入字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 打印结果，便于课堂展示
for key, value in result.items():
    print(f"{key}: {value:.6f}")

# 如果直接运行脚本，result 已可用
