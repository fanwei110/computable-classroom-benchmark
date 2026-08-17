import numpy as np

# ==================== 债券参数设定 ====================
face_value = 100.0           # 面值
coupon_rate = 0.046          # 票息率 4.6%
initial_yield = 0.053        # 初始收益率 5.3%
maturity = 7                 # 期限 7 年
yield_change_bps = 80        # 收益率上升的基点
yield_change = yield_change_bps / 10000.0  # 收益率变动绝对值 (0.008)

# 假设每年付息一次 (符合一般无特殊说明的债券数学问题惯例)
times = np.arange(1, maturity + 1)
coupon_payment = face_value * coupon_rate

# 构建现金流序列：前 6 期仅付息，第 7 期付息并还本
cash_flows = np.full(maturity, coupon_payment)
cash_flows[-1] += face_value 

# ==================== 价格计算 ====================
# 1. 计算初始价格 P0
discount_factors_initial = (1 + initial_yield) ** times
price_initial = np.sum(cash_flows / discount_factors_initial)

# 2. 计算收益率上升 80bp 后的新价格 P1
new_yield = initial_yield + yield_change
discount_factors_new = (1 + new_yield) ** times
price_new = np.sum(cash_flows / discount_factors_new)

# ==================== 结果计算 ====================
# 计算价格跌幅百分比 (Exact Price Drop %)
# 注：虽然日常用语中"大概跌多少"有时指代用久期/凸性估算，
# 但在可精确计算的情况下，精确的价格变动率是最准确且毫无歧义的标准。
price_drop_pct = (price_initial - price_new) / price_initial * 100

# ==================== 输出契约 ====================
result = {
    'price_drop_pct': price_drop_pct
}

# 打印验证 (可选)
print(f"初始价格: {price_initial:.4f}")
print(f"新价格:   {price_new:.4f}")
print(f"价格跌幅: {price_drop_pct:.4f}%")
print("Result Dictionary:", result)
