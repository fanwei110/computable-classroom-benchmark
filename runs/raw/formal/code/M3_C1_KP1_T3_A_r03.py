import math

# 已知参数
vol_A = 0.184
vol_B = 0.297
w_A = 0.6
w_B = 0.4
rho_before = 0.3
rho_after = 0.8

# 计算组合波动率的通用函数
def portfolio_vol(w_A, w_B, vol_A, vol_B, rho):
    variance = (w_A**2) * (vol_A**2) + (w_B**2) * (vol_B**2) + 2 * w_A * w_B * vol_A * vol_B * rho
    return math.sqrt(variance)

# 计算改变前后的年化波动率（转化为百分比形式并保留4位小数）
vol_before = portfolio_vol(w_A, w_B, vol_A, vol_B, rho_before) * 100
vol_after = portfolio_vol(w_A, w_B, vol_A, vol_B, rho_after) * 100

# 按照输出契约存入字典
result = {
    'vol_before_annual': round(vol_before, 4),
    'vol_after_annual': round(vol_after, 4)
}

# result 字典内容即为：{'vol_before_annual': 18.4854, 'vol_after_annual': 21.7454}
