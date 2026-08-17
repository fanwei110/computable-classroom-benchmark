import numpy as np

# 债券参数
face_value = 100.0       # 面值
coupon_rate = 0.046      # 票息率
maturity = 7             # 年限
ytm = 0.053              # 到期收益率

# 每年付息一次（未指定时默认为年付息）
coupon = face_value * coupon_rate

# 现金流时间点（第1年到第7年）
t = np.arange(1, maturity + 1)   # 1,2,...,7

# 现金流：每年票息 + 最后一年本金
cf = np.full(maturity, coupon)
cf[-1] += face_value             # 最后一年票息+本金

# 贴现因子
discount = (1 + ytm) ** t
pv_cf = cf / discount

# 1. 价格
price = np.sum(pv_cf)

# 2. 麦考利久期
weight = pv_cf / price
macaulay_duration = np.sum(t * weight)

# 修正久期（年复利）
modified_duration = macaulay_duration / (1 + ytm)

# 3. 凸性
# 公式：Convexity = [ ∑ t(t+1) * PV(CF_t) ] / [ (1+y)^2 * P ]
t_t1 = t * (t + 1)
convexity = np.sum(t_t1 * pv_cf) / ((1 + ytm) ** 2 * price)

# 存储结果
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 输出以供课堂投屏
print(result)
