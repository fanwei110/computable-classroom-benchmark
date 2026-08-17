import math

# 已知参数
vol_A = 0.184
vol_B = 0.297
w_A = 0.6
w_B = 0.4

# 相关系数变化前
rho_before = 0.3
var_before = (w_A ** 2) * (vol_A ** 2) + (w_B ** 2) * (vol_B ** 2) + 2 * w_A * w_B * vol_A * vol_B * rho_before
vol_before = math.sqrt(var_before)

# 相关系数变化后
rho_after = 0.8
var_after = (w_A ** 2) * (vol_A ** 2) + (w_B ** 2) * (vol_B ** 2) + 2 * w_A * w_B * vol_A * vol_B * rho_after
vol_after = math.sqrt(var_after)

# 转换为百分比并保留两位小数
result = {
    'vol_before_annual': round(vol_before * 100, 2),
    'vol_after_annual': round(vol_after * 100, 2)
}
