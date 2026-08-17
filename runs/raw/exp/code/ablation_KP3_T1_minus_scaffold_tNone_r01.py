import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize  # 实际上这里未直接使用，但根据要求引入

# ---------- 输入参数 ----------
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 (小数)
coupon = face_value * coupon_rate  # 每年票息额
maturity_years = 7          # 期限
ytm = 0.053                 # 到期收益率 (小数)
# ------------------------------

# 生成现金流时间点（年）：第1年到第7年
t = np.arange(1, maturity_years + 1)  # [1,2,3,4,5,6,7]

# 现金流：前6年每年为coupon，最后一年为coupon+面值
cf = np.where(t < maturity_years, coupon, coupon + face_value)

# 贴现因子
discount_factor = (1 + ytm) ** (-t)

# 现金流现值
pv = cf * discount_factor

# 价格 = 所有现值之和
price = np.sum(pv)

# ---------- 麦考利久期 ----------
# 麦考利久期 = Σ [ t * PV(CF_t) ] / Price
macaulay_duration = np.sum(t * pv) / price

# ---------- 修正久期 ----------
modified_duration = macaulay_duration / (1 + ytm)

# ---------- 凸性 ----------
# 凸性 = Σ [ t(t+1) * CF_t / (1+y)^(t+2) ] / Price
convexity_numerator = np.sum(t * (t + 1) * cf / ((1 + ytm) ** (t + 2)))
convexity = convexity_numerator / price

# ---------- 结果存入字典 ----------
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 打印所有结果（保留足够精度用于展示）
print("债券价格（现值）    : {:.6f}".format(result['price']))
print("麦考利久期（年）    : {:.6f}".format(result['macaulay_duration_years']))
print("修正久期（年）      : {:.6f}".format(result['modified_duration_years']))
print("凸性（年²）         : {:.6f}".format(result['convexity']))

# 如果需要直观显示现金流表（可选）
# df = pd.DataFrame({
#     '年数': t,
#     '现金流': cf,
#     '贴现因子': discount_factor,
#     '现值': pv
# })
# print("\n现金流现值表：")
# print(df)
