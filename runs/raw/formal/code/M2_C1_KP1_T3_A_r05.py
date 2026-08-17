import math

# ç»å®åæ°
sigma_A = 0.184  # 18.4%
sigma_B = 0.297  # 29.7%
w_A = 0.6
w_B = 0.4
rho_before = 0.3
rho_after = 0.8

# ç»åæ¹å·®åæ³¢å¨çè®¡ç®å½æ°
def portfolio_vol(w_a, sigma_a, w_b, sigma_b, rho):
    var = (w_a * sigma_a)**2 + (w_b * sigma_b)**2 + 2 * w_a * sigma_a * w_b * sigma_b * rho
    return math.sqrt(var)

vol_before = portfolio_vol(w_A, sigma_A, w_B, sigma_B, rho_before)
vol_after = portfolio_vol(w_A, sigma_A, w_B, sigma_B, rho_after)

# å­åå­å
result = {
    'vol_before_annual': vol_before,
    'vol_after_annual': vol_after
}
