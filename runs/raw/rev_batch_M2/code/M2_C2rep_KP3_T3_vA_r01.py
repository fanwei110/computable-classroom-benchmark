import numpy as np

# 债券参数
face_value = 100.0          # 面值
coupon_rate = 0.046         # 票息率（年化）
ytm = 0.053                 # 到期收益率（年化）
years = 7                   # 剩余期限（年）
delta_y = 0.008             # 收益率上升幅度（80个基点）

# 生成现金流时间序列 (假设每年付息一次，按年复利)
t = np.arange(1, years + 1)                     # 现金流发生的年份 1..7
coupon = face_value * coupon_rate               # 每年票息
cf = np.full(years, coupon)                     # 前6年只有票息
cf[-1] += face_value                            # 最后一年加上本金

# 贴现计算
df = (1 + ytm) ** (-t)          # 贴现因子
pv = cf * df                     # 每期现金流现值
price = np.sum(pv)               # 债券当前价格

# 麦考利久期 (MacD = Σ t * PV_t / P)
mac_duration = np.sum(t * pv) / price

# 修正久期 (ModD = MacD / (1 + y))
mod_duration = mac_duration / (1 + ytm)

# 凸性 (C = Σ t(t+1) * PV_t / [P * (1 + y)^2])
convexity = np.sum(t * (t + 1) * pv) / (price * (1 + ytm)**2)

# 近似价格变动百分比 (ΔP/P ≈ -ModD * Δy + 0.5 * C * Δy^2)
delta_p_pct = -mod_duration * delta_y + 0.5 * convexity * (delta_y ** 2)

# 价格下跌百分比（将 ΔP/P 的负值转为正数跌幅，并换成百分比形式）
price_drop_pct = -delta_p_pct * 100   # 例如 delta_p_pct = -0.045 -> price_drop_pct = 4.5

# 按照输出契约组织结果
result = {
    'price_drop_pct': price_drop_pct
}

print(result)
