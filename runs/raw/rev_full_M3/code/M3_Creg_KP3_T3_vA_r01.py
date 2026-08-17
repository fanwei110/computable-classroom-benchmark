import numpy as np

# ==================== 债券参数设置 ====================
face_value = 100.0                  # 面值
coupon_rate = 0.046                 # 票息率 (4.6%)
initial_yield = 0.053               # 初始收益率 (5.3%)
maturity = 7                        # 期限 (7年)
yield_change_bps = 80               # 收益率上升的点数 (基点)
yield_change = yield_change_bps / 10000.0  # 转换为绝对数值 (0.008)

# ==================== 现金流构造 ====================
# 默认按年付息（若为半年付息需调整期数与折现率，题干未特别说明则按年处理）
coupon_payment = face_value * coupon_rate
cash_flows = np.full(maturity, coupon_payment)
cash_flows[-1] += face_value  # 最后一期加上面值本金

# 对应的折现期数
time_periods = np.arange(1, maturity + 1)

# ==================== 价格计算 ====================
# 计算初始价格 P0
discount_factors_initial = (1 + initial_yield) ** time_periods
initial_price = np.sum(cash_flows / discount_factors_initial)

# 计算收益率上升 80 个基点后的新价格 P1
new_yield = initial_yield + yield_change
discount_factors_new = (1 + new_yield) ** time_periods
new_price = np.sum(cash_flows / discount_factors_new)

# ==================== 计算价格下跌百分比 ====================
price_drop_pct = (initial_price - new_price) / initial_price

# ==================== 输出契约 ====================
result = {
    'price_drop_pct': price_drop_pct
}

# 打印结果以便直观查看
if __name__ == "__main__":
    print(f"初始价格: {initial_price:.4f}")
    print(f"收益率上升后新价格: {new_price:.4f}")
    print(f"价格大概下跌: {price_drop_pct:.4%}")
    print(f"输出字典: {result}")
