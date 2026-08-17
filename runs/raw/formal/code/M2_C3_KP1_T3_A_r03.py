import math

# 输入参数
sigma_A = 0.184
sigma_B = 0.297
w_A = 0.6
w_B = 0.4
rho_before = 0.3
rho_after = 0.8

# 计算组合方差与波动率
var_A = sigma_A ** 2
var_B = sigma_B ** 2
cov_term = 2 * w_A * w_B * sigma_A * sigma_B

var_before = w_A**2 * var_A + w_B**2 * var_B + rho_before * cov_term
var_after = w_A**2 * var_A + w_B**2 * var_B + rho_after * cov_term

vol_before_annual = math.sqrt(var_before)
vol_after_annual = math.sqrt(var_after)

result = {
    'vol_before_annual': vol_before_annual,
    'vol_after_annual': vol_after_annual
}
print(result)
