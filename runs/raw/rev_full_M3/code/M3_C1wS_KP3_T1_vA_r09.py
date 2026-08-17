import numpy as np

# ==========================================
# 债券定价与久期、凸性计算
# ==========================================

# --- 假设处理 ---
# 题目未指明付息频率，采用金融市场与《证券投资学》教学中最常用的惯例：按年付息 (Annual Coupon)。
# 到期收益率(YTM)为年化名义收益率，与付息频率一致。

# --- 债券基本参数 ---
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票面利率 4.6%
years_to_maturity = 7       # 期限 7年
ytm = 0.053                # 到期收益率 5.3%

# --- 步骤1：计算现金流与价格 ---
# 生成时间序列 t = 1, 2, ..., 7
t = np.arange(1, years_to_maturity + 1)

# 构建现金流向量：前6期为票息，第7期为票息+面值
cash_flows = np.full(years_to_maturity, face_value * coupon_rate)
cash_flows[-1] += face_value

# 贴现因子
discount_factors = (1 + ytm) ** -t

# 价格 = 现金流贴现之和
price = np.sum(cash_flows * discount_factors)

# --- 步骤2：计算麦考利久期与修正久期 ---
# 麦考利久期 = (t * 现金流 * 贴现因子) 之和 / 价格
weighted_pv = t * cash_flows * discount_factors
macaulay_duration = np.sum(weighted_pv) / price

# 修正久期 = 麦考利久期 / (1 + 到期收益率)
modified_duration = macaulay_duration / (1 + ytm)

# --- 步骤3：计算凸性 ---
# 凸性公式 = (1/P) * SUM[ CF_t * t * (t+1) / (1+y)^(t+2) ]
convexity_numerator = cash_flows * t * (t + 1) * (1 + ytm) ** -(t + 2)
convexity = np.sum(convexity_numerator) / price

# --- 步骤4：填充 result ---
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# ==========================================
# 课堂展示输出
# ==========================================
if __name__ == '__main__':
    print("=" * 45)
    print("《证券投资学》- 债券定价与久期/凸性计算")
    print("=" * 45)
    print(f"面值: {face_value} | 票面利率: {coupon_rate*100}% | 期限: {years_to_maturity}年 | YTM: {ytm*100}%")
    print("-" * 45)
    # 格式化输出，保留6位小数以保证精度展示
    for key, value in result.items():
        print(f"{key:<28} {value:>10.6f}")
    print("=" * 45)
