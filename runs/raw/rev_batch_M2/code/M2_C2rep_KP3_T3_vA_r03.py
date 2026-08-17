import math

# 债券参数
face_value = 100.0       # 面值
coupon_rate = 0.046      # 票息率（年）
yield_rate = 0.053       # 到期收益率（年）
maturity = 7             # 年限（年）
delta_y = 0.008          # 收益率变动：80个基点（+0.8%）

# 生成现金流：假设每年付息一次
cash_flows = []
for t in range(1, maturity):
    cash_flows.append((t, face_value * coupon_rate))
cash_flows.append((maturity, face_value * coupon_rate + face_value))

# 计算价格、麦考利久期和凸性所需求和项
price = 0.0
mac_dur_num = 0.0  # 麦考利久期分子 Σ t * PV(CF)
conv_num = 0.0     # 凸性分子 Σ t*(t+1) * PV(CF)

for t, cf in cash_flows:
    pv_cf = cf / ((1 + yield_rate) ** t)
    price += pv_cf
    mac_dur_num += t * pv_cf
    conv_num += t * (t + 1) * pv_cf

# 麦考利久期
mac_dur = mac_dur_num / price
# 修正久期
mod_dur = mac_dur / (1 + yield_rate)
# 凸性
convexity = conv_num / (price * (1 + yield_rate) ** 2)

# 估算价格变动百分比：ΔP/P ≈ -MD*Δy + 0.5*Conv*(Δy)^2
delta_p_pct = -mod_dur * delta_y + 0.5 * convexity * (delta_y ** 2)

# 跌幅为正数（价格下跌的百分比）
price_drop_pct = -delta_p_pct * 100.0  # 转换为百分比并取正

# 存储结果
result = {'price_drop_pct': round(price_drop_pct, 6)}

# 输出以便课堂查看
print("债券定价与利率敏感性估算")
print(f"面值: {face_value}, 票息: {coupon_rate*100}%, 收益率: {yield_rate*100}%")
print(f"当前价格: {price:.6f}")
print(f"麦考利久期: {mac_dur:.6f} 年")
print(f"修正久期: {mod_dur:.6f}")
print(f"凸性: {convexity:.6f}")
print(f"收益率上升 {delta_y*100} 个基点时，价格变动近似为 {delta_p_pct*100:.4f}%")
print(f"预估价格跌幅: {price_drop_pct:.4f}%")
print("\n最终结果字典:")
print(result)
