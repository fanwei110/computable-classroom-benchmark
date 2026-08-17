import math

# 输入参数
sigma_A = 0.184
sigma_B = 0.297
w_A = 0.6
w_B = 0.4
rho_before = 0.3
rho_after = 0.8

# 组合方差与波动率计算
var_before = (w_A**2 * sigma_A**2 +
              w_B**2 * sigma_B**2 +
              2 * w_A * w_B * rho_before * sigma_A * sigma_B)
vol_before = math.sqrt(var_before)

var_after = (w_A**2 * sigma_A**2 +
             w_B**2 * sigma_B**2 +
             2 * w_A * w_B * rho_after * sigma_A * sigma_B)
vol_after = math.sqrt(var_after)

result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}
