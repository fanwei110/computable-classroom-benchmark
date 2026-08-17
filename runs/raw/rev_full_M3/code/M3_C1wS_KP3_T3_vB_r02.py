import numpy as np

# ==========================================
# 1. 基础参数与假设设定
# ==========================================
# 题目给出的债券参数
face_value = 100         # 面值
coupon_rate = 0.046      # 票息率 4.6%
ytm = 0.053              # 当前到期收益率 5.3%
maturity = 7             # 期限 7年
delta_y = 0.008          # 收益率上升 80个基点 (80 bps)

# 假设处理：
# 1. 付息频率：题目未指明，按中国国内主流附息国债惯例，假设为【每年付息一次】。
# 2. 期限计算：假设当前正好处于付息日，剩余期限为完整的7年。
t = np.arange(1, maturity + 1)

# 构建现金流：前6期只有票息，第7期包含票息和本金
cash_flows = np.full(maturity, face_value * coupon_rate)
cash_flows[-1] += face_value

# ==========================================
# 2. 计算该债券在当前收益率下的利率敏感性
# ==========================================
discount_factors = (1 + ytm) ** (-t)
price = np.sum(cash_flows * discount_factors)

# 麦考利久期
mac_duration = np.sum(t * cash_flows * discount_factors) / price

# 修正久期 = - (1/P) * (dP/dy)
mod_duration = mac_duration / (1 + ytm)

# 凸性 = (1/P) * (d^2P/dy^2)
convexity = np.sum(t * (t + 1) * cash_flows * (1 + ytm)**(-t - 2)) / price

# ==========================================
# 3. 估算收益率上升 80bp 的价格影响
# ==========================================
# 根据泰勒展开式，价格变化率近似为：
# ΔP/P ≈ - 修正久期 × Δy + 0.5 × 凸性 × (Δy)^2
price_drop_pct = -mod_duration * delta_y + 0.5 * convexity * (delta_y ** 2)

# ==========================================
# 4. 结果存储与课堂投屏展示
# ==========================================
result = {'price_drop_pct': price_drop_pct}

# 辅助验证：计算真实贴现价格变动，以供课堂对比讲解久期/凸性的近似效果
new_ytm = ytm + delta_y
new_discount_factors = (1 + new_ytm) ** (-t)
new_price = np.sum(cash_flows * new_discount_factors)
actual_drop_pct = (new_price - price) / price

print(f"【计算前提】面值: {face_value}, 票息率: {coupon_rate*100}%, 期限: {maturity}年, 付息频率: 每年一次")
print(f"【当前状态】到期收益率: {ytm*100}%, 债券价格: {price:.4f}元")
print(f"【敏感性指标】修正久期: {mod_duration:.4f}年, 凸性: {convexity:.4f}")
print("-" * 55)
print(f"【估算结果】收益率上升80bp时，久期+凸性估算跌幅: {price_drop_pct*100:.4f}%")
print(f"【精确验证】收益率上升80bp时，现金流贴现实际跌幅: {actual_drop_pct*100:.4f}%")
print("-" * 55)
print(f"最终输出字典 result: {result}")
