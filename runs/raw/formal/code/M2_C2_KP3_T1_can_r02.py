import numpy as np

# 债券参数
face_value = 100.0         # 面值
coupon_rate = 0.046        # 票息率 4.6%
years = 7                  # 期限 7 年
ytm = 0.053                # 到期收益率 5.3%

# 生成现金流时间点 (1 ~ 7 年，按年付息)
t = np.arange(1, years + 1)

# 现金流向量：每年票息，最后一年加上本金
coupon = face_value * coupon_rate
cash_flows = np.full(years, coupon)
cash_flows[-1] += face_value   # 最后一期现金流 = 票息 + 本金

# 1. 计算价格：现金流贴现之和
discount_factors = (1 + ytm) ** t
pv_cash_flows = cash_flows / discount_factors
price = np.sum(pv_cash_flows)

# 2. 麦考利久期：加权平均时间，权重为各期现金流现值占总价格的比例
weights = pv_cash_flows / price
macaulay_duration = np.sum(t * weights)

# 修正久期
modified_duration = macaulay_duration / (1 + ytm)

# 3. 凸性（修正凸性）
# 公式：Convexity = (1 / Price) * Σ [ t*(t+1)*CF_t / (1+ytm)^(t+2) ]
# 等价于 Σ [ t*(t+1) * pv_cash_flows ] / (Price * (1+ytm)^2 )
convexity_numerator = np.sum(t * (t + 1) * pv_cash_flows)
convexity = convexity_numerator / (price * (1 + ytm)**2)

# 将结果存入字典
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# 打印输出以供课堂投屏查看
if __name__ == "__main__":
    for key, val in result.items():
        print(f"{key}: {val:.6f}")
