import numpy as np

# ================= 债券参数设定 =================
# 题目未指明付息频率，这里采用金融市场最常见的假设：每年付息1次
face_value = 100.0         # 面值
coupon_rate = 0.046        # 票息率 4.6%
years = 7                  # 期限 7 年
ytm = 0.053                # 到期收益率 5.3%
freq = 1                   # 每年付息次数

# ================= 1. 计算价格 =================
# 生成各期现金流的时间序列 (1, 2, ..., 7)
t = np.arange(1, years * freq + 1)

# 生成各期现金流：每期票息，最后一期加上面值
cf = np.full(years * freq, face_value * coupon_rate / freq)
cf[-1] += face_value

# 计算贴现因子与现金流现值
discount_rate = 1 + ytm / freq
pv_cf = cf / (discount_rate ** t)

# 价格为现金流现值之和
price = np.sum(pv_cf)

# ================= 2. 计算麦考利久期与修正久期 =================
# 麦考利久期 = 各期现金流现值加权时间 / 价格 (除以freq转化为年)
macaulay_duration_years = np.sum(t * pv_cf) / (price * freq)

# 修正久期 = 麦考利久期 / (1 + 到期收益率/付息频率)
modified_duration_years = macaulay_duration_years / discount_rate

# ================= 3. 计算凸性 =================
# 凸性的标准金融定义：Conv = 1/(P * freq^2) * Σ [ t(t+1) * CF / (1+y/freq)^(t+2) ]
# 这样计算出的凸性可以直接用于泰勒展开式：ΔP/P ≈ -ModD*Δy + 0.5*Conv*(Δy)^2
convexity = np.sum(t * (t + 1) * cf / (discount_rate ** (t + 2))) / (price * freq ** 2)

# ================= 4. 填充 result =================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration_years,
    'modified_duration_years': modified_duration_years,
    'convexity': convexity
}

# 课堂投屏友好输出
print("="*50)
print("《证券投资学》- 债券定价与久期、凸性计算")
print("="*50)
print(f"参数设定: 面值={face_value}, 票息率={coupon_rate*100}%, 期限={years}年, YTM={ytm*100}%, 频率={freq}次/年")
print("-"*50)
for key, value in result.items():
    print(f"{key:>28s} : {value:.6f}")
print("="*50)
