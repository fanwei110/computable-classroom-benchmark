import numpy as np

# ==================== 债券参数 ====================
face_value = 100          # 面值
coupon_rate = 0.046       # 票息率 4.6%
ytm = 0.053               # 当前到期收益率 5.3%
n_years = 7               # 期限 7年
delta_y = 0.008           # 收益率上升 80 个基点 (0.80%)

# ==================== 1. 计算当前价格与利率敏感性 ====================
# 构建现金流
coupon = face_value * coupon_rate
cash_flows = np.full(n_years, coupon)
cash_flows[-1] += face_value  # 最后一期包含本金

# 时间序列
time_periods = np.arange(1, n_years + 1)

# 现值与当前价格
present_values = cash_flows / (1 + ytm) ** time_periods
current_price = np.sum(present_values)

# 麦考利久期 (Macaulay Duration)
mac_duration = np.sum(time_periods * present_values) / current_price

# 修正久期 (Modified Duration)
mod_duration = mac_duration / (1 + ytm)

# 凸性 (Convexity)
# P = sum(CF_t / (1+y)^t) -> dP/dy = -sum(t*CF_t / (1+y)^(t+1))
# d2P/dy2 = sum(t*(t+1)*CF_t / (1+y)^(t+2))
# 凸性 C = (1/P) * d2P/dy2
convexity = np.sum(time_periods * (time_periods + 1) * cash_flows / (1 + ytm) ** (time_periods + 2)) / current_price

# ==================== 2. 估算收益率上升80bp的价格影响 ====================
# 使用久期与凸性进行二阶泰勒展开估算：
# ΔP/P ≈ -ModD * Δy + (1/2) * Convexity * (Δy)^2
price_drop_pct = -mod_duration * delta_y + 0.5 * convexity * (delta_y ** 2)

# ==================== 3. 把跌幅存入 result ====================
# 注：price_drop_pct 为负数，代表价格下跌的百分比变化率
result = {
    'price_drop_pct': price_drop_pct
}

# (可选) 打印结果以供验证
if __name__ == "__main__":
    print(f"当前价格: {current_price:.4f}")
    print(f"修正久期: {mod_duration:.4f}")
    print(f"凸性: {convexity:.4f}")
    print(f"估算价格变化百分比: {result['price_drop_pct']:.4%}")
