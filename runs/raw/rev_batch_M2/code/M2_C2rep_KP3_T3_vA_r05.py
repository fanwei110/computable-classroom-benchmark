import numpy as np

# 债券参数
face_value = 100.0
coupon_rate = 0.046  # 票息率 4.6%
yield_to_maturity = 0.053  # 到期收益率 5.3%
maturity_years = 7  # 期限 7 年
delta_y = 0.0080  # 收益率上升 80 个基点
freq = 1  # 假设每年付息一次（内部一致假设，便于课堂展示）

# 现金流时间点（年）
t = np.arange(1, maturity_years * freq + 1) / freq
# 每期票息
coupon = face_value * coupon_rate / freq
# 现金流向量（最后一期包含本金）
cash_flows = np.full(len(t), coupon)
cash_flows[-1] += face_value

# 贴现因子
discount = 1 / (1 + yield_to_maturity / freq) ** (t * freq)
# 债券当前价格
price = np.sum(cash_flows * discount)

# 麦考利久期
macaulay_duration = np.sum(t * cash_flows * discount) / price
# 修正久期
modified_duration = macaulay_duration / (1 + yield_to_maturity / freq)

# 凸性（年化）
# 标准凸性公式: (1/价格) * sum( t*(t+1/freq)*现金流 / (1+y/freq)^(t*freq+2) )
# 对于 freq=1 简化为 t*(t+1) 和 t+2 次方
time_factor = t * (t + 1 / freq)
convexity = np.sum(time_factor * cash_flows / 
                   (1 + yield_to_maturity / freq) ** (t * freq + 2)) / price

# 价格百分比变化（泰勒展开二阶近似）
price_change_pct_approx = (-modified_duration * delta_y + 
                           0.5 * convexity * delta_y ** 2) * 100

# 精确价格变化（用于验证，但不要求输出）
new_yield = yield_to_maturity + delta_y
discount_new = 1 / (1 + new_yield / freq) ** (t * freq)
price_new = np.sum(cash_flows * discount_new)
price_change_pct_exact = (price_new - price) / price * 100

# 跌幅（正数表示下跌的百分比）
price_drop_pct = -price_change_pct_approx

# 结果字典
result = {'price_drop_pct': round(price_drop_pct, 4)}

# 打印关键结果，便于课堂投屏
print(f"债券当前价格: {price:.4f}")
print(f"修正久期: {modified_duration:.4f}")
print(f"凸性: {convexity:.4f}")
print(f"收益率上升 {delta_y*100:.0f} 个基点")
print(f"近似价格变化: {price_change_pct_approx:.4f}%")
print(f"精确价格变化: {price_change_pct_exact:.4f}%")
print(f"估算跌幅 (price_drop_pct): {price_drop_pct:.4f}%")
print(f"result = {result}")
