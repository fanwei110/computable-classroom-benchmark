import numpy as np

# ==================== 债券参数设定 ====================
# 题目信息："7年的债（100/4.6%/5.3%）"，收益率上升80bp
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率 4.6%
ytm = 0.053                # 当前到期收益率 5.3%
maturity = 7               # 期限 7年
delta_y = 80 / 10000       # 收益率上升 80 个基点 (0.008)

# 假设：按年付息（最标准的教材假设），现金流在每年年末发生
periods = np.arange(1, maturity + 1)
cash_flows = np.full(maturity, face_value * coupon_rate)
cash_flows[-1] += face_value  # 最后一期包含本金

# ==================== 1. 计算当前价格与利率敏感性 ====================
# 贴现因子
discount_factors = (1 + ytm) ** periods

# 各期现金流现值
pv_cf = cash_flows / discount_factors

# 债券当前价格
price = np.sum(pv_cf)

# 麦考利久期
mac_duration = np.sum(periods * pv_cf) / price

# 修正久期 - 衡量一阶敏感性
mod_duration = mac_duration / (1 + ytm)

# 凸性 - 衡量二阶敏感性
# 公式: Conv = (1/P) * sum[ t(t+1) * CF / (1+y)^(t+2) ]
convexity = np.sum(periods * (periods + 1) * cash_flows / ((1 + ytm) ** (periods + 2))) / price

# ==================== 2. 估算收益率上升80bp的价格影响 ====================
# 使用久期与凸性进行二阶近似估算
# dP/P ≈ -ModD * dy + 0.5 * Conv * dy^2
price_change_pct = -mod_duration * delta_y + 0.5 * convexity * (delta_y ** 2)

# 跌幅（正数表示下跌的幅度）
price_drop_pct = -price_change_pct

# ==================== 3. 结果存入 result ====================
result = {
    'price_drop_pct': price_drop_pct
}

# (可选) 课堂投屏辅助打印，便于教师讲解
print(f"--- 债券定价与久期、凸性计算 ---")
print(f"当前到期收益率: {yym*100:.1f}%" if 'yym' in dir() else "") # 防错处理，直接用ytm
print(f"当前到期收益率: {ytm*100:.1f}%")
print(f"债券当前价格: {price:.4f} 元")
print(f"麦考利久期: {mac_duration:.4f} 年")
print(f"修正久期: {mod_duration:.4f}")
print(f"凸性: {convexity:.4f}")
print(f"---------------------------------")
print(f"收益率变动: +{delta_y*10000:.0f} bp")
print(f"久期一阶影响: {-mod_duration * delta_y * 100:.4f}%")
print(f"凸性二阶影响: {0.5 * convexity * (delta_y ** 2) * 100:.4f}%")
print(f"预估总价格变动: {price_change_pct*100:.4f}%")
print(f"预估跌幅: {price_drop_pct*100:.4f}%")
print(f"=================================")
print(f"结果字典 result: {result}")
