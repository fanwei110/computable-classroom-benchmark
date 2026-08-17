import numpy as np

# ==================== 假设与参数设置 ====================
# 假设：由于题目未指明付息频率，按中国《证券投资学》课程惯例，默认为年度付息 (m=1)
face_value = 100.0        # 面值
coupon_rate = 0.046       # 票息率 4.6%
years_to_maturity = 7     # 期限 7 年
ytm = 0.053               # 到期收益率 5.3%

# ==================== 1. 计算债券价格 ====================
# 生成各期时间点 (1 到 7 年)
t = np.arange(1, years_to_maturity + 1)

# 生成各期现金流：前 6 期仅为票息，第 7 期为票息+面值
cash_flows = np.full(years_to_maturity, face_value * coupon_rate)
cash_flows[-1] += face_value

# 计算贴现因子
discount_factors = (1 + ytm) ** t

# 价格 = 现金流贴现之和
price = np.sum(cash_flows / discount_factors)

# ==================== 2. 计算麦考利久期与修正久期 ====================
# 各期现金流的现值
pv_cash_flows = cash_flows / discount_factors

# 麦考利久期 = (时间 * 现金流现值) 之和 / 债券价格
macaulay_duration = np.sum(t * pv_cash_flows) / price

# 修正久期 = 麦考利久期 / (1 + 到期收益率)
modified_duration = macaulay_duration / (1 + ytm)

# ==================== 3. 计算凸性 ====================
# 凸性 = (各期 t*(t+1)*现金流 / (1+y)^(t+2)) 之和 / 债券价格
# 注：此处采用标准金融学定义，对应价格二阶导数 P''(y)/P，配合泰勒展开式 ΔP/P ≈ -D*Δy + 0.5*C*(Δy)^2 使用
convexity = np.sum(t * (t + 1) * cash_flows / ((1 + ytm) ** (t + 2))) / price

# ==================== 4. 填充 result ====================
result = {
    'price': price,
    'macaulay_duration_years': macaulay_duration,
    'modified_duration_years': modified_duration,
    'convexity': convexity
}

# (可选) 控制台输出，方便投屏展示
if __name__ == "__main__":
    print("债券定价与久期、凸性计算结果：")
    for key, value in result.items():
        print(f"{key:30s}: {value:.6f}")
