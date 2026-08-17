import math

# 已知参数
vol_A = 0.184
vol_B = 0.297
w_A = 0.6
w_B = 0.4
corr_before = 0.3
corr_after = 0.8

# 计算组合方差和波动率的通用过程
var_A = (w_A * vol_A) ** 2
var_B = (w_B * vol_B) ** 2
cov_base = 2 * w_A * w_B * vol_A * vol_B

# 前状态计算
var_before = var_A + var_B + corr_before * cov_base
vol_before = math.sqrt(var_before)

# 后状态计算
var_after = var_A + var_B + corr_after * cov_base
vol_after = math.sqrt(var_after)

# 按要求存入字典，保留4位小数（即百分比保留2位小数）
result = {
    'vol_before_annual': round(vol_before, 4),
    'vol_after_annual': round(vol_after, 4)
}

# result 值为: {'vol_before_annual': 0.1849, 'vol_after_annual': 0.2175}
# 对应的百分比约为：前 18.49%，后 21.75%
