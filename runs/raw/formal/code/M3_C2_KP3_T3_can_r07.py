import numpy as np

# ==========================================
# 债券参数与假设
# ==========================================
face_value = 100.0       # 面值
coupon_rate = 0.046      # 票息率 4.6%
ytm = 0.053              # 当前收益率 5.3%
maturity = 7             # 期限 7 年
delta_y = 0.008          # 收益率上升 80 个基点 (0.80%)

# 假设：债券按年付息（题目未指明付息频率，采用中国大学金融学常规的年付假设）
freq = 1

# ==========================================
# 1. 计算债券在当前收益率下的价格与利率敏感性 (久期、凸性)
# ==========================================
# 生成现金流时间与金额
t = np.arange(1, maturity + 1)
cf = np.full(maturity, face_value * coupon_rate)
cf[-1] += face_value  # 最后一期加入本金

# 贴现因子
discount_factors = (1 + ytm) ** t

# 债券当前价格
price = np.sum(cf / discount_factors)

# 麦考利久期
mac_duration = np.sum(t * cf / discount_factors) / price

# 修正久期
mod_duration = mac_duration / (1 + ytm)

# 凸性
# 凸性公式: (1/P) * sum[ t*(t+1) * CF / (1+y)^(t+2) ]
convexity = np.sum(t * (t + 1) * cf / discount_factors) / (price * (1 + ytm) ** 2)

# ==========================================
# 2. 估算收益率上升 80 个基点的价格影响
# ==========================================
# 利用久期和凸性估算价格变动百分比:
# dP/P ≈ -ModDur * dy + 0.5 * Conv * dy^2
price_drop_pct = (-mod_duration * delta_y + 0.5 * convexity * delta_y ** 2) * 100

# (附加：计算精确价格跌幅以供课堂对比参考)
price_new = np.sum(cf / (1 + ytm + delta_y) ** t)
actual_drop_pct = (price_new - price) / price * 100

# ==========================================
# 3. 存入结果
# ==========================================
result = {
    'price_drop_pct': price_drop_pct
}

# ==========================================
# 课堂投屏展示打印
# ==========================================
print("="*50)
print("《证券投资学》- 债券定价与久期、凸性估算")
print("="*50)
print(f"债券面值: {face_value} | 票息率: {coupon_rate*100}% | 期限: {maturity}年 | 付息频率: 年付")
print(f"当前收益率: {ytm*100}% | 收益率变动: +{delta_y*10000}bp")
print("-"*50)
print(f"【步骤1】当前债券价格: {price:.4f}")
print(f"【步骤1】麦考利久期:   {mac_duration:.4f} 年")
print(f"【步骤1】修正久期:     {mod_duration:.4f}")
print(f"【步骤1】凸性:         {convexity:.4f}")
print("-"*50)
print(f"【步骤2】久期估算影响: {-mod_duration * delta_y * 100:.4f}%")
print(f"【步骤2】凸性修正影响: {0.5 * convexity * delta_y**2 * 100:.4f}%")
print(f"【步骤2】估算价格跌幅: {price_drop_pct:.4f}%")
print("-"*50)
print(f"[参考] 精确价格跌幅:   {actual_drop_pct:.4f}% (对比观察凸性修正的效果)")
print("="*50)
print(f"输出契约字典 result: {result}")
