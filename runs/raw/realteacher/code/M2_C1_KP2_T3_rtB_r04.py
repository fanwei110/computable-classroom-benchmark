# 计算过程
beta = 1.42
R_m_monthly = -0.058
R_f_annual = 0.047
R_f_monthly = R_f_annual / 12

# CAPM月收益
result = {
    'capm_return_monthly': R_f_monthly + beta * (R_m_monthly - R_f_monthly)
}
