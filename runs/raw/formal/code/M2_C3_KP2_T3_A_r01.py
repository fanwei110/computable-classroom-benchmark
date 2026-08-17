# 计算过程
r_f_annual = 0.047
r_f_monthly = (1 + r_f_annual)**(1/12) - 1
beta = 1.42
r_m = -0.058
capm_return_monthly = r_f_monthly + beta * (r_m - r_f_monthly)

result = {'capm_return_monthly': capm_return_monthly}
