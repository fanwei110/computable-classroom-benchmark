import numpy as np

# ==================== 债券基本参数 ====================
face_value = 100          # 面值
coupon_rate = 0.046       # 票息率 4.6%
yield_rate = 0.053        # 初始收益率 5.3%
n_years = 7               # 期限 7 年
delta_y = 0.008           # 收益率上升 80 个基点 (80 bps)

# ==================== 现金流构建 ====================
# 假设按年付息（未特别说明时的标准设定）
cash_flows = np.array([coupon_rate * face_value] * n_years)
cash_flows[-1] += face_value  # 最后一期加入本金

# 期数序列
periods = np.arange(1, n_years + 1)

# ==================== 精确价格计算 ====================
# 1. 计算初始价格
discount_factors_initial = (1 + yield_rate) ** periods
price_initial = np.sum(cash_flows / discount_factors_initial)

# 2. 计算收益率上升 80bps 后的新价格
yield_new = yield_rate + delta_y
discount_factors_new = (1 + yield_new) ** periods
price_new = np.sum(cash_flows / discount_factors_new)

# 3. 计算精确的价格下跌百分比
exact_price_drop_pct = (price_initial - price_new) / price_initial

# ==================== 久期与凸性估算（作为“大概”跌幅的对照） ====================
# 现值
pv_cash_flows_initial = cash_flows / discount_factors_initial

# 麦考利久期与修正久期
mac_duration = np.sum(periods * pv_cash_flows_initial) / price_initial
mod_duration = mac_duration / (1 + yield_rate)

# 使用修正久期的一阶估算（固定收益中常指的“大概跌幅”）
approx_drop_duration = mod_duration * delta_y

# 凸性及二阶估算
convexity = np.sum(periods * (periods + 1) * pv_cash_flows_initial) / (price_initial * (1 + yield_rate)**2)
approx_drop_dur_conv = mod_duration * delta_y - 0.5 * convexity * delta_y**2

# ==================== 输出契约 ====================
# 存入精确的真实价格跌幅（代表真实的下跌幅度），同时也提供久期近似值作为参考
result = {
    'price_drop_pct': exact_price_drop_pct
}

# ==================== 打印详情 ====================
print(f"债券初始价格: {price_initial:.4f}")
print(f"收益率上升 80bps 后价格: {price_new:.4f}")
print(f"-" * 40)
print(f"【精确】价格下跌百分比: {exact_price_drop_pct:.4%}")
print(f"【久期一阶估算】大概跌幅: {approx_drop_duration:.4%}")
print(f"【久期+凸性估算】大概跌幅: {approx_drop_dur_conv:.4%}")
print(f"-" * 40)
print(f"结果字典: {result}")
