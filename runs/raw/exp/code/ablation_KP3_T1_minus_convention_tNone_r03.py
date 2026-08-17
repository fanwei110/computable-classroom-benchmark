import numpy as np

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
maturity_years = 7          # 剩余期限
ytm = 0.053                 # 到期收益率 5.3%

# 1. 价格计算：每年现金流贴现
coupon = face_value * coupon_rate   # 每年票息 4.6
t = np.arange(1, maturity_years + 1)  # 年份 1..7
# 各期现金流：前6年只付票息，第7年票息+面值
cash_flows = np.full(maturity_years, coupon)
cash_flows[-1] += face_value         # 最后一次加面值

# 按年复利贴现
discount_factors = (1 + ytm) ** (-t)
price = np.sum(cash_flows * discount_factors)

# 2. 麦考利久期 (年)
macaulay_duration = np.sum(t * cash_flows * discount_factors) / price

# 修正久期
modified_duration = macaulay_duration / (1 + ytm)

# 3. 凸性 (年平方)
# 公式: Σ [ t(t+1) * CF_t / (1+y)^(t+2) ] / P
convexity = np.sum(t * (t + 1) * cash_flows / ((1 + ytm) ** (t + 2))) / price

# 4. 按输出契约构建 result 字典
result = {
    'price': round(price, 6),
    'macaulay_duration_years': round(macaulay_duration, 6),
    'modified_duration_years': round(modified_duration, 6),
    'convexity': round(convexity, 6)
}

# 打印结果（教师投屏用）
print("===== 债券定价与久期、凸性计算结果 =====")
print(f"面值: {face_value}")
print(f"票息率: {coupon_rate*100:.2f}%")
print(f"期限: {maturity_years} 年")
print(f"到期收益率: {ytm*100:.2f}%")
print(f"年票息: {coupon:.2f}")
print("----------------------------------------")
print(f"价格 (Price):                    {result['price']:.6f}")
print(f"麦考利久期 (Macaulay Duration):  {result['macaulay_duration_years']:.6f} 年")
print(f"修正久期 (Modified Duration):    {result['modified_duration_years']:.6f} 年")
print(f"凸性 (Convexity):                {result['convexity']:.6f} 年²")

# 验证逻辑（可选，投屏时可展示）
# 敏感性检验：收益率上升1bp，价格变动 ≈ -修正久期*价格*0.0001 + 0.5*凸性*价格*(0.0001)^2
dp_approx = -modified_duration * price * 0.0001 + 0.5 * convexity * price * (0.0001**2)
print("\n--- 敏感性检验 (收益率+1bp) ---")
print(f"久期+凸性近似价格变化: {dp_approx:.6f}")
print(f"直接重定价检验:        {np.sum(cash_flows / (1 + ytm + 0.0001)**t) - price:.6f}")
