import math

# 输入参数
sigma_A = 0.184
sigma_B = 0.297
w_A = 0.6
w_B = 0.4

# 计算组合方差中与相关性无关的部分
base_var = w_A**2 * sigma_A**2 + w_B**2 * sigma_B**2
cov_term = 2 * w_A * w_B * sigma_A * sigma_B

# 相关性变化
rho_before = 0.3
rho_after = 0.8

var_before = base_var + rho_before * cov_term
var_after = base_var + rho_after * cov_term

vol_before = math.sqrt(var_before)
vol_after = math.sqrt(var_after)

result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}
